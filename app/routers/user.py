import time
from fastapi_pagination import paginate, Params
from fastapi import FastAPI, WebSocket
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
from fastapi import APIRouter
from app.common.validation import *

router_user = APIRouter(
    prefix="/user",
    tags=["user-商户管理"],
)


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


# ----
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
                ws = new WebSocket("ws://frps.retailwell.com:20065/user/ws" + "?token=" + token.value);
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


async def get_token(
    websocket: WebSocket,
    token: Union[str, None] = Query(default=None),
):
    if token is None:
        raise Exception(422,'token not found')
    return token


@router_user.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Depends(get_token),
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {token}"
        )

