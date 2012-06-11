import webapp2
import random

from webapp2_extras import sessions
from tweepy.auth import OAuthHandler
from tweepy.api import API

import logging
from model import User

class SessionHandler(webapp2.RequestHandler):
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store()
    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    # Returns a session using the default cookie key.
    return self.session_store.get_session()

class DefaultHandler(SessionHandler):
  def get(self):
    user_id = self.session.get('user')
    if user_id:
      self.response.out.write('You are user {0}'.format(user_id))
    else:
      self.response.out.write('<a href="/auth">Log In! </a>')

class AuthHandler(SessionHandler):
  def get(self):
    #Set up our twitter auth object
    config = self.app.config['twitter']
    auth = OAuthHandler(config['consumer_key'], config['consumer_secret'], self.request.host_url + '/auth')

    tkn = self.session.get('twitter')
    if tkn:
      #If we are on the second phase already
      auth.set_request_token(tkn[0], tkn[1])
      
      del self.session['twitter']

      auth.get_access_token(self.request.get('oauth_verifier'))
      me = API(auth).me()
      results = User.query().filter(User.twitter_id == me.id).fetch()
      if results:
        user = results[0]
      else:
        user = User(twitter_id=me.id, name=me.name, location=me.location, tz=me.time_zone)
        user.put()
      self.session['user'] = user.key.id()
      self.redirect('/')
    else:
      redirect_url = auth.get_authorization_url(signin_with_twitter=True)
      self.session['twitter'] = (auth.request_token.key, auth.request_token.secret)
      self.redirect(redirect_url)
