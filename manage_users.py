import pymongo
import os
import hashlib
import random
import string

MONGO_URL = os.environ.get('MONGOHQ_URL')
if MONGO_URL:
  connection = pymongo.Connection(MONGO_URL, safe=True)
  db = connection[urlparse(MONGO_URL).path[1:]]
else:
  connection = pymongo.Connection('localhost', safe=True)
  db = connection.site
  users = db.users

def check_signup(username, password, pwconf):
  if password != pwconf:
    return "Your passwords do not match"

def make_salt():
  salt = ""
  for i in range(5):
    salt += random.choice(string.ascii_letters)
  return salt

def hash_pw(password, salt=None):
  if salt == None:
    salt = make_salt()
  return hashlib.sha1(password+salt).hexdigest()

def add_user(username, password):
  hashed_pw = hash_pw(password, "salty")
  try:
    users.insert({"_id": username, "password": hashed_pw})
  except pymongo.errors.DuplicateKeyError as e:
    return "Couldn't add you to the database, username exists"
  except:
    return "Pymongo error, retry"
