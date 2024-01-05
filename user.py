from sanic import Blueprint, text
from mycrypt import encrypt, DATABASE_KEY, decrypt
import motor
from sanic.response import json 
from auth import add_user_info_cookie, check_login, is_vip
import requests
from datetime import datetime, timedelta
from config import MONGODB_CONNECTION_STRING
user = Blueprint("user", url_prefix="/api/v1/user")


@user.post("/signup")
async def signup(request):
    if request.form.get('username') is None:
        return json({"status": "error", "msg" : "no username"}, headers={"Access-Control-Allow-Origin": "*"})
    if request.form.get('password') is None:
        return json({"status": "error", "msg" : "no password"}, headers={"Access-Control-Allow-Origin": "*"})

    cf_headers = {"secret": "0x4AAAAAAAOBU8nIWJ4RM7e0hRYFTaCUKBU",
                  "response": request.form.get("cf-turnstile-response"),
                  }
    response = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", data=cf_headers)
    
    json_data = response.json()
    if json_data.get('success'):
        username = request.form.get('username')
        password = request.form.get('password')
        response = json({"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"})
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
        users = client['users']
        users_collection = users['users']
        
        if await users_collection.find_one({'username': request.form.get('username')}) is not None:
            return json({"status": "The user has been signed up!"}, status=200, headers={"Access-Control-Allow-Origin": "*"})
        
        group = "user" if request.form.get("group") is None else request.form.get("group")
        user = {"username": request.form.get('username'), "password": encrypt(request.form.get('password'), key=DATABASE_KEY), "group": group}
        await users_collection.insert_one(user)
        response.cookies['username'] = encrypt(username)
        response.cookies['password'] = encrypt(password)
        return response
    else:
        return json({"status": "error"}, headers={"Access-Control-Allow-Origin": "*"})
        
@user.post("/login")
async def login(request):
    if request.form.get('username') is None:
        return json({"status": "error, no username"}, headers={"Access-Control-Allow-Origin": "*"})
    if request.form.get('password') is None:
        return json({"status": "error, no password"}, headers={"Access-Control-Allow-Origin": "*"})
    username = request.form.get('username')
    password = request.form.get('password')
    cf_headers = {
        "secret": "0x4AAAAAAAOBU8nIWJ4RM7e0hRYFTaCUKBU",
        "response": request.form.get("cf-turnstile-response"),
    }
    response = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", data=cf_headers)
    json_data = response.json()
    if not json_data.get('success'):
        return json({"status": "error"}, headers={"Access-Control-Allow-Origin": "*"})    
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
    users = client['users']
    users_collection = users['users']
    user_document = await users_collection.find_one({'username': username})
    if user_document is None:
        return json({"status": "error", "msg" : "no such user"}, headers={"Access-Control-Allow-Origin": "*"})
    if password == decrypt(user_document['password'], key=DATABASE_KEY):
        response = json({"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"})
        response.cookies['username'] = encrypt(username)
        response.cookies['password'] = encrypt(password)
        return response
    else:
        return json({"status": "error, username or password is wrong"}, headers={"Access-Control-Allow-Origin": "*"})

@user.get("/logout")
async def logout(request):
    past = datetime.now() - timedelta(days=1)
    response = text("ok", headers={"Access-Control-Allow-Origin": "*"})
    response.cookies['username'] = ""
    response.cookies['password'] = ""
    if 'username' in response.cookies:
        response.cookies['username']['expires'] = past
    if 'password' in response.cookies:
        response.cookies['password']['expires'] = past
    return response

@user.get("/check_login")
async def checklogin(request):
    is_authenticated, username = await check_login(request)
    if is_authenticated:
        return json({"login_in": True, "username": username}, headers={"Access-Control-Allow-Origin": "*"})
    else:
        return json({"login_in": False}, headers={"Access-Control-Allow-Origin": "*"})
    
@user.get("/check_vip")
async def check_vip(request):
    is_authenticated, username = await check_login(request)
    if is_authenticated:
        is_vip_user = await is_vip(username)
        return json({"is_vip": is_vip_user}, headers={"Access-Control-Allow-Origin": "*"})
    else:
        return json({"is_vip": False}, headers={"Access-Control-Allow-Origin": "*"})