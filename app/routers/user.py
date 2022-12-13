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


@router_user.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            await websocket.send_bytes(bytes(1))
            time.sleep(1)
        except :
            print('连接断开')
            break

@router_user.get('/test_module')
def test_module(module:str):
    import importlib
    s = importlib.import_module(module)
    return str(s)+'_ok'

