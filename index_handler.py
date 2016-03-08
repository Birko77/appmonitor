import logging
from datetime import date, timedelta
import json
from handler import Handler

from database import Data


class IndexHandler(Handler):
    def get(self):
        self.render('index.html')



class DataHandler(Handler):
    def post(self):
        time_period = int(self.request.get('time_period')) # Number of days (integer)
        region = self.request.get('region') #'US_accumulated' or 'all_states_separate'
        per_day = self.request.get('per_day') #True or False



        raw_data = Data.get_raw_data(time_period)
        if region == 'US_accumulated':
            if per_day == 'True': # series of values over a time period accumulated for the whole country (GRAPH OVER TIME)
                json_obj = []
                for raw_data_item in raw_data:
                    # add first item from raw_data to the empty JSON object
                    if json_obj == []:
                        json_obj.append({'date':str(raw_data_item.date), 
                                         'new_users':raw_data_item.new_users, 
                                         'active_users':raw_data_item.active_users, 
                                         'posts':raw_data_item.posts, 
                                         'chat_messages':raw_data_item.chat_messages, 
                                         'requests':raw_data_item.requests})
                    else:
                        for json_obj_item in json_obj:
                            if str(raw_data_item.date) == json_obj_item['date']:
                                json_obj_item['new_users'] += raw_data_item.new_users
                                json_obj_item['active_users'] += raw_data_item.active_users
                                json_obj_item['posts'] += raw_data_item.posts
                                json_obj_item['chat_messages'] += raw_data_item.chat_messages
                                json_obj_item['requests'] += raw_data_item.requests
                                break
                            elif json_obj.index(json_obj_item) == (len(json_obj)-1):
                                json_obj.append({'date':str(raw_data_item.date), 
                                                 'new_users':raw_data_item.new_users, 
                                                 'active_users':raw_data_item.active_users, 
                                                 'posts':raw_data_item.posts, 
                                                 'chat_messages':raw_data_item.chat_messages, 
                                                 'requests':raw_data_item.requests})
                                break
                global json
                json_string = json.dumps(json_obj)
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write(json_string)
                return
            else: # per_day = 'False': ACCUMULATED values for the whole country and a given time period
                json_obj = {'new_users':0, 'active_users':0, 'posts':0, 'chat_messages':0, 'requests':0, }
                for item in raw_data:
                    for key in json_obj.iterkeys():
                        json_obj[key] += getattr(item, key)
                global json
                json_string = json.dumps(json_obj)
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write(json_string)
                return

        elif region == 'all_states_separate':
            if per_day == 'True': # This would produce series of values over a given time period for each state separately. NOT IMPLEMENTED!
                json_string = '{}'
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write(json_string)
                return
            else: # values accumulated over a given time period, but separate for every state (MAP)
                json_obj = []
                for raw_data_item in raw_data:
                    # add first item from raw_data to the empty JSON object
                    if json_obj == []:
                        json_obj.append({'state':raw_data_item.state, 
                                         'new_users':raw_data_item.new_users, 
                                         'active_users':raw_data_item.active_users, 
                                         'posts':raw_data_item.posts, 
                                         'chat_messages':raw_data_item.chat_messages, 
                                         'requests':raw_data_item.requests})
                    else:
                        for json_obj_item in json_obj:
                            if raw_data_item.state == json_obj_item['state']:
                                json_obj_item['new_users'] += raw_data_item.new_users
                                json_obj_item['active_users'] += raw_data_item.active_users
                                json_obj_item['posts'] += raw_data_item.posts
                                json_obj_item['chat_messages'] += raw_data_item.chat_messages
                                json_obj_item['requests'] += raw_data_item.requests
                                break
                            elif json_obj.index(json_obj_item) == (len(json_obj)-1):
                                json_obj.append({'state':raw_data_item.state, 
                                                 'new_users':raw_data_item.new_users, 
                                                 'active_users':raw_data_item.active_users, 
                                                 'posts':raw_data_item.posts, 
                                                 'chat_messages':raw_data_item.chat_messages, 
                                                 'requests':raw_data_item.requests})
                                break
                global json
                json_string = json.dumps(json_obj)
                self.response.headers['Content-Type'] = 'application/json'
                self.response.write(json_string)
                return

        else:
            return



