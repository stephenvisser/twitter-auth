import webapp2

from webapp2_extras import sessions

class SessionHandler(webapp2.RequestHandler):
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
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
      self.response.out.write('<a href="/auth/twitter">Log In! </a>')

