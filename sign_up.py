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
  food = bottle.request.forms.get('food')

  pw_check = manage_users.check_signup(username, password, pwconf)

  if pw_check == None:
    user_check = manage_users.add_user(username, password, food)
    if user_check == None:
      entry = db.users.find_one({"_id": username})
      hashed_pw = entry["password"]
      #Houston we are a go, the pws match and the user is not in the system
      #THIS IS WHERE THE MAGIC HAPPENS
      session_id = manage_users.start_session(username)
      cookie = manage_users.make_cookie(session_id)
      bottle.response.set_cookie("session", cookie)
      bottle.redirect('/welcome')
    else:
      return bottle.template('signup', dict(pw_error="", user_error=user_check))
  else:
    return bottle.template('signup', dict(pw_error=pw_check, user_error = ""))

def get_session():
  cookie = bottle.request.get_cookie("session")
  if cookie == None:
    print "Sorry, no cookie in the cookie jar"
    return None
  else:
    session_id = manage_users.get_session_from_cookie(cookie)
    if (session_id == None):
      print "Sorry, your cookie didn't generate properly"
    else:
      session = manage_users.get_session_from_db(session_id)
  return session

@bottle.route('/welcome', method='GET')
def say_hello_to_my_friend():
  session = get_session()
  username = session['username']
  user_info = manage_users.get_user_info(username)
  food = user_info['food']
  return "oh hai %s, you like %s" % (username, food)

if os.environ.get('ENVIRONMENT') == 'PRODUCTION':
  port = int(os.environ.get('PORT', 5000))
  print "port = %d" % port
  bottle.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
  bottle.debug(True) #dev only, not for production
  bottle.run(host='localhost', port=8082, reloader=True) #dev only
