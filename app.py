"""
LICENCED WITH GNU AFFERO GENERAL PUBLIC LICENSE (AGPLv3)

Created by Talha Celik
github.com/tlhcelik
github.com/trivelyan-dashboard

"""


from flask import Flask, flash, redirect, render_template, request, session, abort, Markup

import heroku3 as h3 #heroku python API

import os
import sys #for debugger print
import subprocess as s

from deploy_with_languages import DEPLOY_LANG

app = Flask(__name__)

#globals
HEROKU_CONN = ""
STR_APP_LIST = []
#globals

#sessions
#declared from do_login() method
#this declared will do not work because do not https request wherever
#session['API_KEY'] = ""
#session['LOGGED_IN'] = True
#session['STR_APP_LIST'] = []
#sessions

def test_connection (conn):
    """
    this method look at heroku3 api whether is login
    """
    try:
        conn.apps()
        return True
    except Exception as e:
        return False

@app.route('/')
def index():
    if not session.get('LOGGED_IN') or HEROKU_CONN == '':
        return render_template('login.html')
    else:
        return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def do_login():
    global HEROKU_CONN

    api_key = request.form['api_key']
    heroku_conn = h3.from_key(api_key)

    HEROKU_CONN = heroku_conn

    if test_connection(heroku_conn):
        session['LOGGED_IN'] = True
        session['API_KEY'] = api_key
        session['STR_APP_LIST'] = []
    else:
        error_message = Markup("API key is invalid.")
        flash(error_message)
        return render_template('login.html')

    return index()

@app.route("/logout")
def logout():
    global HEROKU_CONN

    session['LOGGED_IN'] = False
    HEROKU_CONN = ''

    return index()

@app.route("/dashboard")
def dashboard():
    get_app_list()

    return render_template('dashboard.html')

@app.route("/user")
def user():
    """
    Get personal user informations
    """
    global HEROKU_CONN
    try:
        email = HEROKU_CONN.account()
    except Exception as e:
        return render_template('login.html')

    email = str(email).split()[1].replace('\'','').replace('>','')
    return render_template('user.html', email = email)

@app.route("/table")
def table():
    STR_APP_LIST, app_list_len = get_app_list()

    return render_template('table.html',
            app_list = STR_APP_LIST,
            app_list_len = app_list_len,
            notify_number = 1
        )

@app.route("/transaction")
def transaction():
    return render_template('transaction.html')

@app.route('/edit', methods=['GET'])
def edit():
    """
    select app from table and click edit button.
    go to edit page with selected app (/edit?app_name=my-app-name)
    """
    if request.method == 'GET':
        app_name = request.args.get('app')

    return render_template('edit.html', app_name = app_name)

@app.route('/save_edit', methods=['GET'])
def save_edit():
    if request.method == 'GET':
        new_app_name = request.args.get('new_app_name')
        old_app_name = request.args.get('old_app_name')
        new_dynos    = request.args.get('new_dynos')

    if new_app_name != '' and old_app_name != '':
        try:
            selected_app = HEROKU_CONN.apps()[old_app_name]
            selected_app.rename(new_app_name)
        except Exception as e:
            return "ERROR 404"

    return table()

@app.route('/deploy_page')
def deploy_page():
    apps, app_list_len = get_app_list()

    return render_template('deploy_page.html', apps=apps, app_list_len=app_list_len)

@app.route('/create_side')
def create_side():
    login_test()
    return render_template('create.html')

@app.route('/delete', methods=['GET'])
def delete():
    """
    Delete your app just with name.
    """
    if request.method == 'GET':
        app_name = request.args.get('delete_app_name')

        try:
            selected_app = HEROKU_CONN.apps()[app_name]
            selected_app.delete()
        except Exception as e:
            return "Error : {0}".format(e)

    return table()

@app.route('/create', methods=['POST', 'GET'])
def create():
    """
    Create your app just with name and region.
    """
    if request.method == 'GET':
        app_name = request.args.get('app_name')
        region_id = request.args.get('region_id')

    try:
        new_app = HEROKU_CONN.create_app(name=str(app_name), region_id_or_name=region_id)
    except Exception as e:
        # go to error page
        return "Some error {0}".format(e)

    return table()

################################################################################
################################################################################
#is not run this method
@app.route('/push_changes', methods=['GET'])
def push_changes(app_name_param = None):
    """
    push your changes selected heroku app
    """
    if app_name_param != None :
        app_name = request.args.get('app_name')
    if request.method == 'GET':
        app_name = request.args.get('app_name')
        commit = request.args.get('commit')
        x = s.check_output(['bash', 'push.sh', app_name])
        return x
        return table()

    return "no"
################################################################################
################################################################################

@app.route('/deploy_with_language', methods=['GET'])
def deploy_with_language():
    if request.method == 'GET':
        app_name = request.args.get('app_name')
        lang = request.args.get('deploy_lang')

        #deployment cli commands
        if lang == DEPLOY_LANG[lang]['name']:
            os.system('mkdir {0}'.format(app_name))
            os.system(DEPLOY_LANG[lang]['command']+' {0}/'.format(app_name)) #download deploy lang repo in to project file
            return push_changes(app_name)
        else:
            return "APP NAME: {0}<hr>LANG: {1}".format(app_name, lang)

def get_app_list():
    """"
    this method get app list with heroku3 library and
    just set global STR_APP_LIST list.
    example :
    STR_APP_LIST[0] -> my-app-Name
    """
    global HEROKU_CONN
    global STR_APP_LIST

    #clear old elements
    del STR_APP_LIST[:]

    try:
        app_list = HEROKU_CONN.apps(order_by='name')
        app_list_len = len(app_list)
    except Exception as e:
        #API key is not declared or losted, try again login
        return render_template('login.html')

    for i in range(app_list_len):
          STR_APP_LIST.append(str(app_list[i]).split()[1].replace('\'',''))

    return STR_APP_LIST, app_list_len

def login_test():
    """
    this method look at whether session is true and whether is open HEROKU_CONN
    """
    if not session.get('LOGGED_IN') and HEROKU_CONN == "":
        return index()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=40)
