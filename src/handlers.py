import webapp2
import random

from webapp2_extras import sessions
from tweepy.auth import OAuthHandler
from tweepy.api import API

import logging

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
      self.response.out.write(API(auth).me().__dict__)
    else:
      redirect_url = auth.get_authorization_url(signin_with_twitter=True)
      logging.getLogger().info(redirect_url)
      self.session['twitter'] = (auth.request_token.key, auth.request_token.secret)
      self.response.out.write('<meta http-equiv="refresh" content="0;url={0}">'.format(redirect_url))
