from google.appengine.ext import ndb

class User(ndb.Model):
  name = ndb.StringProperty(indexed=False)
  twitter_id = ndb.IntegerProperty()
  location = ndb.StringProperty()
