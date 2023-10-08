######################################
# author ben lawson <balawson@bu.edu>
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login
from datetime import date
from datetime import datetime
import itertools
from collections import OrderedDict


#for image uploading
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2308iNg120Ka19'
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users")
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd
	return user

'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
			   <form action='login' method='POST'>
				<input type='text' name='email' id='email' placeholder='email'></input>
				<input type='password' name='password' id='password' placeholder='password'></input>
				<input type='submit' name='submit'></input>
			   </form></br>
			   '''
	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return render_template('hello.html', name = email, message = "Login successful", users = getTopUsers(), tags = getTopTags())

	#information did not match
	return "<a href='/login'>Try again</a>\
			</br> or </br> <a href='/register'>make an account</a>"

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return render_template('hello.html', message='Logged out', users = getTopUsers(), tags = getTopTags())

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html')

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html', supress='True')

@app.route("/register_retry", methods=['GET'])
def register_retry():
	return render_template('register.html')

@app.route("/register", methods=['POST'])
def register_user():
	try:
		email=request.form.get('email')
		password=request.form.get('password')

	except:
		print("couldn't find all tokens") #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		print(cursor.execute("INSERT INTO Users (email,password) VALUES ('{0}','{1}')".format(email, password)))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('hello.html', name=email, message='Account Created!', users = getTopUsers(), tags = getTopTags())
	else:
		print("couldn't find all tokens")
		return flask.redirect(flask.url_for('register_retry'))


def getPhotos():
	cursor = conn.cursor()
	cursor.execute("SELECT data, photo_id, caption FROM Photos")
	return cursor.fetchall()

def getUsersPhotos(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT data, photo_id, caption FROM Photos WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall() #NOTE return a list of tuples, [(imgdata, pid, caption), ...]

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)):
		#this means there are greater than zero entries with that email
		return False
	else:
		return True
#end login code

def getUserFriends(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT email FROM Users WHERE user_id IN (SELECT user_id2 FROM Friends WHERE user_id1 = '{0}') OR user_id IN (SELECT user_id1 FROM Friends WHERE user_id2 = '{0}')".format(uid))
	return cursor.fetchall() 

def getAlbumPhotos(aid):
	cursor = conn.cursor()
	cursor.execute("SELECT data, photo_id, caption FROM Photos WHERE albums_id = '{0}'".format(aid))
	return cursor.fetchall() 

def getUserAlbums(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT name, date FROM Albums WHERE user_id = '{0}'".format(uid))
	return cursor.fetchall() 

def getAlbumIdFromName(name,uid):
	cursor = conn.cursor()
	cursor.execute("SELECT albums_id FROM Albums WHERE name = '{0}' AND user_id = '{1}'".format(name,uid))
	return cursor.fetchone()[0]

def getRecommendedFriends(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT email, COUNT(*) FROM Users U JOIN ((SELECT user_id1 AS user_id FROM Friends F JOIN ((SELECT user_id1 AS user_id2 FROM Friends WHERE user_id2 = '{0}') UNION (SELECT user_id2 AS user_id2 FROM Friends WHERE user_id1 = '{0}')) AS sub1 WHERE F.user_id2 = sub1.user_id2) UNION (SELECT user_id2 AS user_id FROM Friends F JOIN ((SELECT user_id1 AS user_id1 FROM Friends WHERE user_id2 = '{0}' ) UNION (SELECT user_id2 AS user_id1 FROM Friends WHERE user_id1 = '{0}')) AS sub2 WHERE F.user_id1 = sub2.user_id1)) AS sub WHERE U.user_id = sub.user_id AND NOT U.user_id = '{0}' GROUP BY email ORDER BY 2 DESC".format(uid))
	return cursor.fetchall() 

def getPhotoTags(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT tag FROM Tags WHERE photo_id = '{0}'".format(pid))
	return cursor.fetchall() 


def getPhotoComments(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT email, text, date FROM Comments C JOIN Users U WHERE C.user_id = U.user_id AND photo_id = '{0}' ORDER BY 2 DESC".format(pid))
	return cursor.fetchall() 

def getPhotoFromId(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT data, caption, photo_id, email FROM Photos RIGHT JOIN Users ON Users.user_id = Photos.user_id WHERE photo_id = '{0}'".format(pid))
	return cursor.fetchone()

def getPhotos():
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM Photos")
	return cursor.fetchall()

def getLikes(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM Likes WHERE photo_id = '{0}'".format(pid))
	return cursor.fetchone()[0]

def getUsersWhoLiked(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT email FROM Likes L JOIN Users U WHERE L.user_id = U.user_id AND photo_id = '{0}'".format(pid))
	return cursor.fetchall()

def getUserIdWhoLiked(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id FROM Likes WHERE photo_id = '{0}'".format(pid))
	return cursor.fetchall()

def getPhotoOwner(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id FROM Photos WHERE photo_id = '{0}'".format(pid))
	return cursor.fetchone()[0]

def getMostRecentUpload(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT MAX(photo_id) FROM Photos WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getPhotosFromTag(tag):
	cursor = conn.cursor()
	cursor.execute("SELECT data, caption, P.photo_id FROM Photos P JOIN Tags T WHERE T.photo_id = P.photo_id AND T.tag = '{0}'".format(tag))
	return cursor.fetchall()


def getUserPhotosFromTag(tag,uid):
	cursor = conn.cursor()
	cursor.execute("SELECT data, caption, P.photo_id FROM Photos P JOIN Tags T WHERE T.photo_id = P.photo_id AND P.user_id = '{1}' AND T.tag = '{0}'".format(tag,uid))
	return cursor.fetchall()


def getTopUsers():
	cursor = conn.cursor()
	cursor.execute("SELECT U.user_id, email, COUNT(*) FROM Users U RIGHT JOIN ((SELECT user_id FROM Photos) UNION ALL (SELECT user_id FROM Comments)) AS sub ON sub.user_id = U.user_id GROUP BY U.user_id ORDER BY 3 DESC;")
	return cursor.fetchmany(10)

def getTopTags():
	cursor = conn.cursor()
	cursor.execute("SELECT tag, COUNT(*) FROM Tags GROUP BY tag ORDER BY 2 DESC")
	return cursor.fetchmany(10)


def getMatchingComments(comment):
	cursor = conn.cursor()
	cursor.execute("SELECT email, U.user_id, COUNT(*) FROM Users U RIGHT JOIN Comments C ON U.user_id = C.user_id WHERE C.text = '{0}' GROUP BY user_id ORDER BY 2 DESC".format(comment))
	return cursor.fetchall()

def getUserTopTags(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT tag, COUNT(*) FROM Tags T RIGHT JOIN Photos P ON P.photo_id = T.photo_id WHERE P.user_id = '{0}' GROUP BY tag ORDER BY 2 DESC".format(uid))
	return cursor.fetchmany(5)

def getPhotosWithOneMatchingTag(uid,tag1):
	cursor = conn.cursor()
	cursor.execute("SELECT photo_id, COUNT(*) FROM (SELECT P.user_id, P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS a WHERE a.photo_id IN (SELECT P.photo_id FROM (SELECT DISTINCT photo_id FROM Photos) AS P WHERE P.photo_id NOT IN (SELECT DISTINCT photo_id FROM (SELECT * FROM (SELECT DISTINCT PIDs.photo_id, Tags.tag FROM (SELECT DISTINCT photo_id FROM Photos) AS PIDs, (SELECT DISTINCT tag FROM Tags WHERE tag IN ('{1}')) AS Tags) AS CP WHERE NOT EXISTS (SELECT * FROM (SELECT P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS PT WHERE CP.photo_id = PT.photo_id AND CP.tag = PT.tag)) AS RD)) AND NOT a.user_id = '{0}' GROUP BY photo_id ORDER BY 2".format(uid, tag1))
	return cursor.fetchall()

def getPhotosWithTwoMatchingTags(uid,tag1,tag2):
	cursor = conn.cursor()
	cursor.execute("SELECT photo_id, COUNT(*) FROM (SELECT P.user_id, P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS a WHERE a.photo_id IN (SELECT P.photo_id FROM (SELECT DISTINCT photo_id FROM Photos) AS P WHERE P.photo_id NOT IN (SELECT DISTINCT photo_id FROM (SELECT * FROM (SELECT DISTINCT PIDs.photo_id, Tags.tag FROM (SELECT DISTINCT photo_id FROM Photos) AS PIDs, (SELECT DISTINCT tag FROM Tags WHERE tag IN ('{1}','{2}')) AS Tags) AS CP WHERE NOT EXISTS (SELECT * FROM (SELECT P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS PT WHERE CP.photo_id = PT.photo_id AND CP.tag = PT.tag)) AS RD)) AND NOT a.user_id = '{0}' GROUP BY photo_id ORDER BY 2".format(uid, tag1, tag2))
	return cursor.fetchall()

def getPhotosWithThreeMatchingTags(uid,tag1,tag2,tag3):
	cursor = conn.cursor()
	cursor.execute("SELECT photo_id, COUNT(*) FROM (SELECT P.user_id, P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS a WHERE a.photo_id IN (SELECT P.photo_id FROM (SELECT DISTINCT photo_id FROM Photos) AS P WHERE P.photo_id NOT IN (SELECT DISTINCT photo_id FROM (SELECT * FROM (SELECT DISTINCT PIDs.photo_id, Tags.tag FROM (SELECT DISTINCT photo_id FROM Photos) AS PIDs, (SELECT DISTINCT tag FROM Tags WHERE tag IN ('{1}','{2}','{3}')) AS Tags) AS CP WHERE NOT EXISTS (SELECT * FROM (SELECT P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS PT WHERE CP.photo_id = PT.photo_id AND CP.tag = PT.tag)) AS RD)) AND NOT a.user_id = '{0}' GROUP BY photo_id ORDER BY 2".format(uid, tag1, tag2, tag3))
	return cursor.fetchall()

def getPhotosWithFourMatchingTags(uid,tag1,tag2,tag3,tag4):
	cursor = conn.cursor()
	cursor.execute("SELECT photo_id, COUNT(*) FROM (SELECT P.user_id, P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS a WHERE a.photo_id IN (SELECT P.photo_id FROM (SELECT DISTINCT photo_id FROM Photos) AS P WHERE P.photo_id NOT IN (SELECT DISTINCT photo_id FROM (SELECT * FROM (SELECT DISTINCT PIDs.photo_id, Tags.tag FROM (SELECT DISTINCT photo_id FROM Photos) AS PIDs, (SELECT DISTINCT tag FROM Tags WHERE tag IN ('{1}','{2}','{3}','{4}')) AS Tags) AS CP WHERE NOT EXISTS (SELECT * FROM (SELECT P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS PT WHERE CP.photo_id = PT.photo_id AND CP.tag = PT.tag)) AS RD)) AND NOT a.user_id = '{0}' GROUP BY photo_id ORDER BY 2".format(uid, tag1, tag2, tag3, tag4))
	return cursor.fetchall()

def getPhotosWithFiveMatchingTags(uid,tag1,tag2,tag3,tag4,tag5):
	cursor = conn.cursor()
	cursor.execute("SELECT photo_id, COUNT(*) FROM (SELECT P.user_id, P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS a WHERE a.photo_id IN (SELECT P.photo_id FROM (SELECT DISTINCT photo_id FROM Photos) AS P WHERE P.photo_id NOT IN (SELECT DISTINCT photo_id FROM (SELECT * FROM (SELECT DISTINCT PIDs.photo_id, Tags.tag FROM (SELECT DISTINCT photo_id FROM Photos) AS PIDs, (SELECT DISTINCT tag FROM Tags WHERE tag IN ('{1}','{2}','{3}','{4}','{5}')) AS Tags) AS CP WHERE NOT EXISTS (SELECT * FROM (SELECT P.photo_id, tag FROM Photos P RIGHT JOIN Tags T ON P.photo_id = T.photo_id) AS PT WHERE CP.photo_id = PT.photo_id AND CP.tag = PT.tag)) AS RD)) AND NOT a.user_id = '{0}' GROUP BY photo_id ORDER BY 2".format(uid, tag1, tag2, tag3, tag4, tag5))
	return cursor.fetchall()


def getCombinations(tags,num):
	combinations = []
	for subset in itertools.combinations(tags, num):
		combinations = combinations + [subset]
	return combinations

def getSuggestions(uid):
	tags = getUserTopTags(uid)
	if (len(tags) < 5):
		return "not enough tags"
	else:
		clean_tags = []
		for tag in tags:
			clean_tags = clean_tags + [tag[0]]
		clean_tags = tuple(clean_tags)
		pids = getPhotosWithFiveMatchingTags(uid,clean_tags[0],clean_tags[1],clean_tags[2],clean_tags[3],clean_tags[4])
		ret = []
	
		fourtags=getCombinations(clean_tags,4)
		threetags=getCombinations(clean_tags,3)
		twotags=getCombinations(clean_tags,2)
		onetag=getCombinations(clean_tags,1)

		for tags in fourtags:
			pids = pids + getPhotosWithFourMatchingTags(uid,tags[0],tags[1],tags[2],tags[3])
		for tags in threetags:
			pids = pids + getPhotosWithThreeMatchingTags(uid,tags[0],tags[1],tags[2])
		for tags in twotags:
			pids = pids + getPhotosWithTwoMatchingTags(uid,tags[0],tags[1])
		for tags in onetag:
			pids = pids + getPhotosWithOneMatchingTag(uid,tags[0])

		pids = list(OrderedDict.fromkeys(pids))
		for pid in pids:
			ret = ret + [getPhotoFromId(pid[0])]
		return ret


def getUserInfo(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT first_name, last_name, email, birth_date, hometown, gender FROM Users WHERE user_id = '{0}'".format(uid))
	return cursor.fetchone()


@app.route('/profile', methods = ['GET', 'POST'])
@flask_login.login_required
def protected():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	if request.method == 'POST':
		return render_template('edit_profile.html', info = getUserInfo(uid))
	else:
		return render_template('profile.html', user = getUserInfo(uid))

@app.route('/edit_profile', methods = ['GET', 'POST'])
@flask_login.login_required
def edit_profile():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	if request.method == 'POST':
		fname = request.form.get('first_name')
		lname = request.form.get('last_name')
		gender = request.form.get('gender')
		hometown = request.form.get('hometown')
		bday = request.form.get('birth_date')

		cursor = conn.cursor()

		if (fname != ''):
			cursor.execute('''UPDATE Users SET first_name = %s WHERE user_id = %s''', (fname, uid))
		if (lname != ''):
			cursor.execute('''UPDATE Users SET last_name = %s WHERE user_id = %s''', (lname, uid))
		if (gender != ''):
			cursor.execute('''UPDATE Users SET gender = %s WHERE user_id = %s''', (gender, uid))
		if (hometown != ''):
			cursor.execute('''UPDATE Users SET hometown = %s WHERE user_id = %s''', (hometown, uid))
		if (bday != ''):
			cursor.execute('''UPDATE Users SET birth_date = %s WHERE user_id = %s''', (bday, uid))
		
		conn.commit()
		return render_template('profile.html', user = getUserInfo(uid))
	else:
		return render_template('edit_profile.html', info = getUserInfo(uid))


@app.route('/rec')
@flask_login.login_required
def recommendations():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	suggestions = getSuggestions(uid)
	if suggestions == "not enough tags":
		return render_template('rec.html', message = "You don't have enough tags yet! Recommendations will be available once you have at least 5 tags", tags = getUserTopTags(uid))
	else:
		return render_template('rec.html', photos = suggestions, base64 = base64, tags = getUserTopTags(uid), title = "You may also like: " )

@app.route('/friends',methods=['GET'])
@flask_login.login_required
def friends():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	return render_template('friends.html', friends = getUserFriends(uid))

@app.route('/add_friends',methods=['GET','POST'])
@flask_login.login_required
def add_friend():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	if request.method == 'POST':
		user_email = request.form.get('add_friend')
		uid2 = getUserIdFromEmail(user_email)
		if uid == uid2:
			return render_template('add_friends.html', users = getUserList(), message = "cannot add yourself as a friend")
		cursor = conn.cursor()
		cursor.execute('''INSERT INTO Friends (user_id1, user_id2) VALUES (%s, %s)''', (uid, uid2))
		conn.commit()
		return render_template('friends.html', friends = getUserFriends(uid))
	else:
		return render_template('add_friends.html', users = getUserList()[1:],recommended = getRecommendedFriends(uid))

@app.route('/search_comments', methods=['GET','POST'])
def search_comments():
	if request.method == 'POST':
		comment = request.form.get('comment')
		return render_template('search_comments.html', comments = getMatchingComments(comment), search = comment)
	else:
		return render_template('search_comments.html')

@app.route('/browse', methods=['GET','POST'])
def browse():
	if request.method == 'POST':
		tags = request.form.get('tags')
		tag_list = tags.split(" ")
		photos = ()
		print(photos)
		for tag in tag_list:
			print(tag)
			photos = photos + getPhotosFromTag(tag)
			photos = list(OrderedDict.fromkeys(photos))
			photos = tuple(photos)
		return render_template('search.html', photos = photos, base64 = base64, tags = tags)
	else:
		return render_template('browse.html', photos = getPhotos(), base64 = base64)

#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/<album>', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file(album):
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		caption = request.form.get('caption')
		aid= getAlbumIdFromName(album,uid)
		photo_data =imgfile.read()
		cursor = conn.cursor()
		cursor.execute('''INSERT INTO Photos (data, albums_id, user_id, caption) VALUES (%s, %s, %s ,%s)''', (photo_data, aid, uid, caption))
		conn.commit()
		pid = getMostRecentUpload(uid)
		return render_template('tag.html', photo = getPhotoFromId(pid), base64=base64)
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		return render_template('upload.html',album = album)
#end photo uploading code

@app.route("/tag/<pid>", methods = ['POST'])
@flask_login.login_required
def tag(pid):
	uid = getUserIdFromEmail(flask_login.current_user.id)
	tags = request.form.get('tags')
	tag_list = tags.replace(" ","").split("#")[1:]
	cursor = conn.cursor()
	for tag in tag_list:
		cursor.execute('''INSERT INTO Tags (photo_id, tag) VALUES (%s, %s)''', (pid, tag))
	conn.commit()	
	return render_template('photo.html', photo = getPhotoFromId(pid), comments = getPhotoComments(pid), tags = getPhotoTags(pid), base64=base64, like = getLikes(pid))


@app.route("/likes/<pid>", methods=['GET'])
@flask_login.login_required
def likes(pid):
	return render_template('likes.html', photo = getPhotoFromId(pid), base64=base64, likes = getUsersWhoLiked(pid)) 


@app.route("/photo/<pid>", methods=['GET','POST'])
def photo(pid):
	if request.method == 'POST':
		today = date.today()
		text = request.form.get('comment')
		if (flask_login.current_user.is_anonymous):
			uid = 1
		else: 
			uid = getUserIdFromEmail(flask_login.current_user.id)	
		if (uid == getPhotoOwner(pid)):
			return render_template('photo.html', photo = getPhotoFromId(pid), comments = getPhotoComments(pid), tags = getPhotoTags(pid), base64=base64, like = getLikes(pid), message = "You can't comment on your own photo")
		else:
			cursor = conn.cursor()
			cursor.execute('''INSERT INTO Comments (user_id, photo_id, text, date) VALUES (%s, %s, %s, %s)''', (uid, pid, text,today))
			conn.commit()
			return render_template('photo.html', photo = getPhotoFromId(pid), comments = getPhotoComments(pid), tags = getPhotoTags(pid), base64=base64, like = getLikes(pid))
	else:
		return render_template('photo.html', photo = getPhotoFromId(pid), comments = getPhotoComments(pid), tags = getPhotoTags(pid), base64=base64, like = getLikes(pid))

@app.route("/like/<pid>", methods=['POST'])
@flask_login.login_required
def like(pid):
	uid = getUserIdFromEmail(flask_login.current_user.id)
	if (uid in getUserIdWhoLiked(pid)):
		return render_template('photo.html', photo = getPhotoFromId(pid), comments = getPhotoComments(pid), tags = getPhotoTags(pid), base64=base64, like = getLikes(pid), message = "You already liked this photo")
	else:
		
		cursor = conn.cursor()
		cursor.execute('''INSERT INTO Likes (photo_id, user_id) VALUES (%s, %s)''', (pid, uid))
		conn.commit()
		return render_template('photo.html', photo = getPhotoFromId(pid), comments = getPhotoComments(pid), tags = getPhotoTags(pid), base64=base64, like = getLikes(pid))

@app.route("/search/<tag>", methods=['GET'])
def search(tag):
	return render_template('search.html', photos = getPhotosFromTag(tag), base64 = base64, tags = tag)

@app.route("/album/<name>", methods=['GET'])
@flask_login.login_required
def album(name):
	clean_name = name[1:-1]
	uid = getUserIdFromEmail(flask_login.current_user.id)
	aid = getAlbumIdFromName(clean_name,uid)
	return render_template('album.html', aid = aid, album = clean_name, photos = getAlbumPhotos(aid),base64=base64)

@app.route("/albums", methods=['GET','POST'])
@flask_login.login_required
def albums():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	if request.method == 'POST':
		tags = request.form.get('tags')
		tag_list = tags.split(" ")
		photos = ()
		print(photos)
		for tag in tag_list:
			print(tag)
			photos = photos + getUserPhotosFromTag(tag,uid)
		return render_template('search.html', photos = photos, base64 = base64, tags = tags)
	else:
		return render_template('albums.html', albums = getUserAlbums(uid))

@app.route("/new_album", methods=['GET', 'POST'])
@flask_login.login_required
def create_album():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		album_name = request.form.get('album_name')
		today = date.today()
		cursor = conn.cursor()
		cursor.execute('''INSERT INTO Albums (name, user_id, date) VALUES (%s, %s, %s)''', (album_name,uid,today))
		conn.commit()
		return render_template('albums.html', albums = getUserAlbums(uid))
	else: 
		return render_template('new_album.html')

@app.route("/delete_album/<aid>", methods=['GET'])
@flask_login.login_required
def delete_album(aid):
	uid = getUserIdFromEmail(flask_login.current_user.id)
	cursor = conn.cursor()
	cursor.execute('''DELETE FROM Albums WHERE albums_id = '{0}' '''.format(aid))
	conn.commit()
	return render_template('albums.html', albums = getUserAlbums(uid))

@app.route("/home", methods=['GET'])
@flask_login.login_required
def home():
	return render_template('hello.html', name=flask_login.current_user.id, users = getTopUsers(), tags = getTopTags())

#default page
@app.route("/", methods=['GET'])
def hello():
	return render_template('unauth.html')


if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port=5000, debug=True)
