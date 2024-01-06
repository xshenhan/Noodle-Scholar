from sanic import Blueprint, response
from sanic.response import json, text
from openai import OpenAI
from auth import protected, vip_protected
import motor
from bson.objectid import ObjectId
from sanic.request import Request
from openai import OpenAI
from json import dumps
import os
from utils import get_collection
from config import *

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE_URL)
model = Blueprint("model", url_prefix="/api/v1/model")

def read_json_part(file_path, size):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read(size)
        return content


@model.route("/summary", methods=["GET"])
@vip_protected
async def summary(request):
    # 检查是否提供了 paper_id
    if request.args.get("id") is None:
        return json({"error": "must request with a paper id"}, status=416, headers={"Access-Control-Allow-Origin": "*"})

    source = request.args.get("source", "100pdfs")
    paper_id = request.args.get("id")

    # 连接 MongoDB 数据库
    collection = get_collection(source)
    document = await collection.find_one({"_id": ObjectId(paper_id)})
    
    if document is None:
        return json({"error": "no such paper"}, status=416, headers={"Access-Control-Allow-Origin": "*"})
    
    if source == "arxiv" or True:
        # paper_url = f"https://arxiv.org/pdf/{document['id']}.pdf"
        # msg = [
        #     {"role": "system", "content": "The user will give you a url of a paper, you should first read it carefully and then write a summary of it as short as possible. And then user will ask you a few questions. You should help the user with some questions about this paper. And you should answer in Chinese as default."},
        #     {"role": "user", "content": f"Here is the url of the paper: {paper_url}. What's the paper mainly about?"}
        # ]
        # model_type = request.args.get("model_type", "gpt-3.5-turbo")
        model_type = request.args.get("model_type", "gpt-3.5-turbo-16k")
        # print(paper_url)
        msg = [
            {"role": "system", "content": f"Here is a paper named {document['title']} and its abstact is {document['abstract']}. You should first read it carefully and then write a summary of it based on your knowledge, title and the abstarct. Then user will ask you a few questions. You should help the user with some questions about this paper. Answer in Chinese as default. Always answer as short as possible. I will tip you 100 dollar if your answer is short enough."},
            {"role": "user", "content": f"What's the paper mainly about?"},
        ]
    elif source == "100pdfs":
        paper_content = read_json_part(document["edited_text_address"], 5000)
        print(paper_content)
        msg  = [
            {"role": "system", "content": "The user will give you some contents of a paper, you should first read it and then write a summary of it as short as possible. And then user will ask you a few questions. You should help the user with some questions about this paper. And you should answer in Chinese as default."},
            {"role": "user", "content": f"Here is the content of the paper: {paper_content}."}
        ]
        model_type = request.args.get("model_type", "gpt-3.5-turbo-16k")
    else:
        return json({"error": "not implemented"}, status=416, headers={"Access-Control-Allow-Origin": "*"})


    # 构建历史记录和请求
    history = {
        "model": model_type,
        "message": msg
    }

    # 构建提示


    # 调用 OpenAI API
    response = client.chat.completions.create(model=model_type,
    messages=history["message"],
    max_tokens=5000)
    answer = response.choices[0].message.content
    print("model output: ", answer)
    # 将结果添加到历史记录并返回
    history["message"].append({"role": "assistant", "content": answer})
    
    return json(history, headers={"Access-Control-Allow-Origin": "*"})

@model.route("/qa", methods=["GET", "POST"])
@vip_protected
async def ask_openai(request: Request):
    if request.method == "GET":
        return response.json({"error": "NOT IMPLEMENTED"}, status=416, headers={"Access-Control-Allow-Origin": "*"})
    # 获取请求数据
    data = request.json
    question = data.get("question")
    history = data.get("history", None)
    if history is None:
        if data.get("message") is None:
            return json({"error":"message is required"}, headers={"Access-Control-Allow-Origin": "*"})
        message = data.get("message")
        history = {
            "model": data.get("model", "gpt-3.5-turbo"),
            "message": message
        }

    # 添加用户的问题到提示
    # 调用 OpenAI API
    response = client.chat.completions.create(model=history["model"],
    messages=history["message"],
    max_tokens=5000)
    answer = response.choices[0].message.content

    # 将回答添加到历史记录并返回
    history["message"].append({"role": "user", "content": question})
    history["message"].append({"role": "assistant", "content": answer})
    return json(history, headers={"Access-Control-Allow-Origin": "*"})

@model.get("/tests")
@protected
async def tests(request):
    model_type = request.args.get("model_type") if request.args.get("model_type") is not None else "gpt-3.5-turbo"
    completion = client.chat.completions.create(
        model=model_type,
        messages=[
            {"role": "system", "content": f"Just say hi to the user"},
            {"role": "user", "content": f"Just say hi to me."},
        ]
    )
    # return json(completion, headers={"Access-Control-Allow-Origin": "*"})
    return text(completion.choices[0].message.content, headers={"Access-Control-Allow-Origin": "*"})

