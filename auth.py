from functools import wraps
from mycrypt import decrypt, encrypt, DATABASE_KEY
from sanic import text, html
import motor

async def check_login(request):
    if not request.cookies.get('username', None):
        return False, "no username"
    if not request.cookies.get('password', None):
        return False, "no password"

    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    users = client['users']
    users_collection = users['users']
    users_doc = await users_collection.find_one({'username': decrypt(request.cookies.get('username'))})
    if users_doc and decrypt(request.cookies.get('password')) == decrypt(users_doc['password'], key=DATABASE_KEY):
        return True, decrypt(request.cookies.get('username'))
    return False, "username or password is wrong"

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated, _ = await check_login(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                # 设置延迟时间（以毫秒为单位）
                delay_ms = 500  # 例如，3秒
                # 设置重定向的目标 URL
                redirect_url = "/login"
                # 返回包含 JavaScript 的 HTML 响应
                return html(f"""
                <html>
                    <head>
                        <script type="text/javascript">
                            setTimeout(function() {{
                                window.location = '{redirect_url}';
                            }}, {delay_ms});
                        </script>
                    </head>
                    <body>
                        <p>You are unauthorized. You will be redirected in {delay_ms / 1000} seconds.</p>
                    </body>
                </html>
                """, status=401)

        return decorated_function

    return decorator(wrapped)

async def is_vip(username):
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    users = client['users']
    users_collection = users['users']
    users_doc = await users_collection.find_one({'username': decrypt(username)})
    if users_doc:
        return users_doc['vip'] == "Y" if 'vip' in users_doc else False
    return False
    
def vip_protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated, _ = await check_login(request)

            if is_authenticated:
                if await is_vip(request.cookies.get('username')):
                    response = await f(request, *args, **kwargs)
                    return response
                else:
                    delay_ms = 1500
                    redirect_url = "/"
                    return html(f"""
                    <html>
                        <head>
                            <script type="text/javascript">
                                setTimeout(function() {{
                                    window.location = '{redirect_url}';
                                }}, {delay_ms});
                            </script>
                        </head>
                        <body>
                            <p>You are not a vip, please contact the superuser. You will be redirected in {delay_ms / 1000} seconds.</p>
                        </body>
                    </html>
                    """, status=401)
            else:
                # 设置延迟时间（以毫秒为单位）
                delay_ms = 500  # 例如，3秒
                # 设置重定向的目标 URL
                redirect_url = "/signup"
                # 返回包含 JavaScript 的 HTML 响应
                return html(f"""
                <html>
                    <head>
                        <script type="text/javascript">
                            setTimeout(function() {{
                                window.location = '{redirect_url}';
                            }}, {delay_ms});
                        </script>
                    </head>
                    <body>
                        <p>You are unauthorized. You will be redirected in {delay_ms / 1000} seconds.</p>
                    </body>
                </html>
                """, status=401)

        return decorated_function

    return decorator(wrapped)

def add_user_info_cookie(func):
    async def wrapper(request, *args, **kwargs):
        response = await func(request, *args, **kwargs)
        response.cookies['username'] = encrypt(request.args.get('username'))
        response.cookies['password'] = encrypt(request.args.get('password'))
        return response
    return wrapper

