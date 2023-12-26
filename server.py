import sanic
from sanic import Sanic, response
from sanic_session import Session
from sanic.response import text, redirect, json, ResponseStream, file_stream, file, html
import motor
import motor.motor_asyncio
from bson.objectid import ObjectId
from sanic_cors import CORS
from auth import protected, add_user_info_cookie, vip_protected
from query import PaperSearch
from mycrypt import encrypt, decrypt, DATABASE_KEY
from os.path import isfile, join
import requests
from paper import paper as paper_bp
from search import search as search_bp
from model import model as model_bp
from user import user as user_bp
from sanic_ext import Extend
from visualization import visualization as visualization_bp
app = Sanic("ns")
Session(app)
Extend(app)
origins = [
    "*"
]

app.config["CORS_RESOURCES"] = {r"/*": {"origins": origins}}
CORS(app)

app.static('/assets', './dist/assets')

app.blueprint(paper_bp)
app.blueprint(user_bp)
app.blueprint(search_bp)
app.blueprint(model_bp)
app.blueprint(visualization_bp)

@app.get("/")
async def root(request):
    # '''the root page will be redirect to test page(we will change in future)'''
    return await file("./dist/index.html")
    
@app.get("/test")
async def test(request):
    # ''' just to test that the api server is working
    # ''' 
    # return text("Hello world!", headers={"Access-Control-Allow-Origin": "*"})
    return await file("./tests/index.html")

# @app.get("/api/v1/paper/lists")
# async def get_lists(requests):
@app.get("/secret")
@protected
async def secert(request):
    return text("secret")
    
@app.get("/secret/vip")
@vip_protected
async def secert_vip(request):
    return text("secret vip !!!!")
    
# 处理前端路由
@app.route('/<path:path>')
async def catch_all(request, path):
    file_path = join('./dist', path)
    # 如果请求的是静态文件，则返回该文件
    if isfile(file_path):
        return await file(file_path)
    # 否则，返回 Vue 应用的 index.html，让 Vue Router 处理路由+
    return await file('./dist/index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, dev=True)
    # app.run(host="0.0.0.0", port=8080, debug=False, access_log=False, fast=True)
