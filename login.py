from sanic import Blueprint, text
from mycrypt import encrypt, DATABASE_KEY
import motor

login = Blueprint("login", url_prefix="/login")


@login.post("/")
async def do_login(request):
    if request.args.get('username') is None:
        return text('You should provide a username')
    if request.args.get('password') is None:
        return text('You should provide a password')
    
    response = text('Welcome. Login Success!')
    response.cookies['username'] = encrypt(request.args.get('username'))
    response.cookies['password'] = encrypt(request.args.get('password'))
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    users = client['users']
    users_collection = users['users']
    group = "user" if request.args.get("group") is None else request.args.get("group")
    user = {"username": encrypt(request.args.get('username'), key=DATABASE_KEY), "password": encrypt(request.args.get('password'), key=DATABASE_KEY), "group": group}
    await users_collection.insert_one(user)
    return response