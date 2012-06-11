from handlers.page import DefaultHandler
from handlers.auth import ProviderHandler

import webapp2

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'ksld8923h89fihf02ih0eifjh02ih084h0f8h208h0hfis972'
    }

app = webapp2.WSGIApplication([
  (r'/', DefaultHandler),
  (r'/auth/(.*)', ProviderHandler)], debug=True, config=config)
