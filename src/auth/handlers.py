import webapp2
import random

from webapp2_extras import sessions
from tweepy.auth import OAuthHandler
from tweepy.api import API

from model import User

class SessionHandler(webapp2.RequestHandler):
  '''
  A base class for any handlers interested in
  saving session state.
  '''   
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
  '''
  This is just an example handler for the 
  main page.
  '''
  def get(self):
    user_id = self.session.get('user')
    if user_id:
      self.response.out.write('You are user {0}'.format(user_id))
    else:
      self.response.out.write('<a href="/auth">Log In! </a>')

class AuthHandler(SessionHandler):
  '''
  This is the handler for when the user is logging in
  '''
  def get(self):
    #Set up our twitter auth object
    config = self.app.config['twitter']
    auth = OAuthHandler(config['consumer_key'], config['consumer_secret'], self.request.host_url + '/auth')

    #Check the session state. If it contains a twitter token, 
    #The user has already gone through the authorization step
    tkn = self.session.get('twitter')
    if tkn:
      #If we are on the second phase already
      auth.set_request_token(tkn[0], tkn[1])
      del self.session['twitter']

      verifier = self.request.get('oauth_verifier')
      if verifier:
        #Get the verification code from the URL
        auth.get_access_token(verifier)
        me = API(auth).me()

        #See if we already have a user that has this id.
        results = User.query().filter(User.twitter_id == me.id).fetch()
        if results:
          user = results[0]

          #Make sure all the properties are up-to-date
          user.name = me.name
          user.location = me.location
          user.put()
        else:
          user = User(twitter_id=me.id, name=me.name, location=me.location)
          user.put()
        
        #The user_id should be part of the session
        self.session['user'] = user.key.id()

      self.redirect('/')
    else:
      #Grabs request_tokens and creates a URL for a redirect
      redirect_url = auth.get_authorization_url(signin_with_twitter=True)
      
      #Store the request_token information for the next step
      self.session['twitter'] = (auth.request_token.key, auth.request_token.secret)
      self.redirect(redirect_url)
