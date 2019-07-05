from flask import Flask, render_template, url_for,session, flash, redirect, request, make_response, jsonify
import vk_api
import requests
import json

friendsInfo = list()


app = Flask(__name__)
access_token = ''
user_ids = ''

@app.route("/")

def Home():
    if access_token == '':
        return redirect('http://localhost:5000/Login')
    else:
        return redirect('http://localhost:5000/Friends')

    
@app.route("/Friends")
def Friends():
    global friendsInfo, accountInfo, access_token, user_ids
    
    if access_token == '':
        app = 7041347
        secret = 'ePZOUzAUKPBL37XqOZ5P'
        urlSplit = request.url.split('code=')
        code = urlSplit[-1]
        redirect_url = 'http://localhost:5000/Friends'
        vk_session = vk_api.VkApi(app_id=app, client_secret=secret)
        vk_session.code_auth(code,redirect_url)
        user_ids = vk_session.token['user_id']
        access_token = vk_session.token['access_token']
    try:
        user  = requests.get('https://api.vk.com/method/users.get?user_ids='+str(user_ids)+'&fields=bdate&access_token='+str(access_token)+'&v=5.101').content
        user = json.loads(user)
        accountInfo  = user.get('response')[0]

        friends = requests.get('https://api.vk.com/method/friends.get?user_ids='+str(user_ids)+'&count=5&fields=bdate&access_token='+str(access_token)+'&v=5.101').content
        friends = json.loads(friends)
        friendsInfo = friends.get('response').get('items')
    except:
        access_token = "" 
        return redirect('http://localhost:5000/Login')

    return render_template('Friends.html', friendsInfo = friendsInfo, accountInfo = accountInfo)


@app.route("/Friends",  methods=['POST'])
def FriendsPost():
    global access_token, user_ids

    ret = {'user_ids': user_ids, 'access_token': access_token}
    return jsonify(ret)


@app.route("/Login")
def Login():
    return render_template('Login.html')


@app.route("/Login", methods=['POST'])

def LoginPOST():
    global access_token, user_ids

    try:
        reqVk =  request.form['vk_session']
        reqVk = json.loads(reqVk)
        
    except:
        access_token = ''
        user_ids = ''
        
        return redirect('https://oauth.vk.com/authorize?client_id=7041347&display=page&redirect_uri=http://localhost:5000/Friends')


    access_token = reqVk.get('access_token')
    user_ids = reqVk.get('user_ids')
    
    return redirect('http://localhost:5000/Friends')

    

