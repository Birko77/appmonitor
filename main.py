import webapp2

from index_handler import IndexHandler, DataHandler


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/get_data', DataHandler)
    ], debug = False)


