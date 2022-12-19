import time
from fastapi_pagination import paginate, Params
from app import schemas, crud
from utils import web_try, sxtimeit, get_utc_now
from fastapi import APIRouter, WebSocket
from app.common.validation import *
from configs.settings import config
import asyncio


router_user = APIRouter(
    prefix="/user",
    tags=["user-商户管理"],
)
PING_INTERVAL = config.get('USER','ping_interval')
LOGIN_EXPIRED = config.get('USER', 'login_expired')


@router_user.post("/create", summary="创建商户")
@web_try()
@sxtimeit
def add_user(item: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, item=item)


@router_user.post("/login", summary="商户登录")
@web_try()
@sxtimeit
def login_user(item: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db=db, item=item)


@router_user.post("/swagger/login", response_model=TokenSchemas, summary="商户登录")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    item = schemas.UserLogin(**{'name': form_data.username, 'password': form_data.password})
    return crud.login_user_swagger(db=db, item=item)


@router_user.put("/user", summary="更新商户信息")
@web_try()
@sxtimeit
def update_user(update_item: schemas.UserUpdate, db: Session = Depends(get_db),
                user: models.User = Depends(check_user)):
    return crud.update_user(db=db, item_id=user.id, update_item=update_item)


@router_user.get("", summary="获取商户列表")
@web_try()
@sxtimeit
def get_users(get_item: schemas.UserGet = Depends(), params: Params = Depends(), db: Session = Depends(get_db),):
    return paginate(crud.get_users(db, get_item), params)


@router_user.get("/getOnce/{item_id}", summary="获取商户信息")
@web_try()
@sxtimeit
def get_user_once(item_id: int, db: Session = Depends(get_db)):
                  # user=Depends(check_admin)):
    return crud.get_user_once(db=db, item_id=item_id)


@router_user.get("/{token}/user_id", summary="获取商户信息")
@web_try()
@sxtimeit
def get_user_id(token: str, db: Session = Depends(get_db)):
    return check_user_id(token, db)


@router_user.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db=Depends(get_db),
    user: models.User = Depends(check_user_ws),
):
    await websocket.accept()
    print(f'客户端连接：user={user.name}')
    await websocket.send_text('1')
    retry = 0
    while True:
        try:
            time.sleep(int(PING_INTERVAL))
            await websocket.send_text('1')
            data = asyncio.wait_for(await websocket.receive_text(), 0.1)
            if data == '0':
                print(f'客户端正常退出,user={user.name}')
                if user.last_ping:
                    user.occupied = 0
                    db.commit()
                    db.flush()
                return
            user.last_ping = time.time()
            user.occupied = 1
            db.commit()
            db.flush()
            retry = 0
        except Exception as e:
            print(f'websocket connect break: retry={retry}, user={user.name}')
            retry += 1
            if retry >= int(LOGIN_EXPIRED)//int(PING_INTERVAL):
                print(f'{retry}次连接失败,客户端关闭,user={user.name},exception:{e}')
                if user.last_ping:
                    user.occupied = 0
                    db.commit()
                    db.flush()
                return









from typing import Union

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    status,
)
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://127.0.0.1:8080/user/ws" + "?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router_user.get("/ws_test")
async def get():
    return HTMLResponse(html)


