
import logging
from datetime import date, timedelta

from google.appengine.ext import db
from google.appengine.api import memcache


class Data(db.Model):

    date = db.DateProperty(required = True)
    state = db.StringProperty(required = True)
    new_users = db.IntegerProperty(required = True)
    active_users = db.IntegerProperty(required = True)
    posts = db.IntegerProperty(required = True)
    chat_messages = db.IntegerProperty(required = True)
    requests = db.IntegerProperty(required = True)
    

    

    @classmethod
    def get_raw_data(cls, days):
        today = date.today() 
        time_delta = timedelta(days=(days))
        starting_date = today - time_delta
        key = str(starting_date)
        d = memcache.get(key)
        if d is None:
            d = Data.all().order('-date').filter('date >', starting_date).fetch(limit=2000)
            memcache.set(key, d)
        return d


