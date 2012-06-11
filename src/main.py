from handlers import DefaultHandler
from handlers import AuthHandler

import webapp2

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'ksld8923h89fihf02ih0eifjh02ih084h0f8h208h0hfis972'
    }

config['twitter'] = {
    'consumer_key': 'DTkW6qicLWKno8xI0RwgiQ',
    'consumer_secret': 'GFNWodOPFhcufAGWoDtHx80J5CyMqFbndPdWLLii0'
    }

app = webapp2.WSGIApplication([
  (r'/', DefaultHandler),
  (r'/auth', AuthHandler)
  ], debug=True, config=config)
