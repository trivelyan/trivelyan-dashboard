from flask import Flask
from flask import render_template
import os
import subprocess as s

app = Flask(__name__)

@app.route('/') #both empty and with name can be come
@app.route('/<name>')
def hello(name=None):
	return render_template('index.html', name=name)

@app.route('/create_file')
@app.route('/create_file/<file_name>')
def create_file(file_name):
	try:
		if (os.path.exists('./'+file_name)): #if file is exists no create and throw except
			return 'File does exist, no created'
		else:#file will created
			cmd = os.system("mkdir "+file_name)
			return "File created"
	except Exception as e:
		return str(e)


@app.route('/login')
def login(name=None):
	"""
	go to ./templates/login/index.html
	"""
	return render_template('login/index.html')
