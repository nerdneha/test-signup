import os
import pymongo
import bottle
import manage_users

from urlparse import urlparse

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
    connection = pymongo.Connection(MONGO_URL, safe=True)
    db = connection[urlparse(MONGO_URL).path[1:]]
else:
  #USE IF USING MONGODB
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.site #replace "database"
users = db.users #replace "collection"

@bottle.route('/')
def default_go_to_signup():
  #eventually ask if there's a cookie so i can redirect to a logged in page
  return bottle.redirect('/signup')

@bottle.route('/signup', method='GET')
def get_user_and_pw():
  return bottle.template('signup', dict(pw_error="", user_error=""))

@bottle.route('/signup', method='POST')
def store_user_and_pw():
  username = bottle.request.forms.get('username')
  password = bottle.request.forms.get('password')
  pwconf = bottle.request.forms.get('passwordconf')

  pw_check = manage_users.check_signup(username, password, pwconf)
  if pw_check == None:
    user_check = manage_users.add_user(username, password)
    if user_check == None:
      entry = db.users.find_one({"_id": username})
      hashed_pw = entry["password"]
      return "Your username is %s, and your password is %s" % (username,
                                                               hashed_pw)
    else:
      return bottle.template('signup', dict(pw_error="", user_error=user_check))
  else:
    return bottle.template('signup', dict(pw_error=pw_check, user_error = ""))

@bottle.route('/welcome', method='GET')
def say_hi():
  return "oh hey there"

if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
  port = int(os.environ.get('PORT', 5000))
  print "port = %d" % port
  bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
  bottle.debug(True) #dev only, not for production
  bottle.run(host='localhost', port=8082, reloader=True) #dev only
