from flask import Flask, render_template, url_for, flash, redirect, request
import vk_api
import requests
import json

friendsInfo = list()

vk_session = None
app = Flask(__name__)



@app.route("/")

def Home():
    global vk_session
    if vk_session is None:
        return redirect(url_for('Login'))
    else:
        return redirect(url_for('Friends'))


@app.route("/Friends")
def Friends():
    global friendsInfo, accountInfo                
    return render_template('Friends.html', friendsInfo = friendsInfo, accountInfo = accountInfo)

@app.route("/Login")
def Login():
    return render_template('Login.html')





@app.route("/Login", methods=['POST'])

def LoginPOST():
    global friendsInfo, accountInfo
    global vk_session
    login = request.form.get('username')
    password = request.form.get('pass')

    try:
            friendsInfo.clear()
            vk_session = vk_api.VkApi(login,password)
            vk_session.auth()
            vk = vk_session.get_api()

            accountInfo = vk.account.getProfileInfo()
            
            friends = vk.friends.get(count=5).get('items')

            for friend in friends:
                friendsInfo.append(vk.users.get(user_ids=friend))
                
    except: 
             vk_session = None   
             return redirect(url_for('Home'))

    
    return redirect(url_for('Friends'))

    