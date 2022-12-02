from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_user = APIRouter(
    prefix="/user",
    tags=["user-商户管理"],
)


# @router_user.post("/create", summary="创建商户")
# @web_try()
# @sxtimeit
# def add_user(item: schemas.UserCreate, db: Session = Depends(get_db)):
#     return crud.create_user(db=db, item=item)


@router_user.post("/login", summary="商户登录")
@web_try()
@sxtimeit
def login_user(item: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db=db, item=item)


@router_user.post("/swagger/login", response_model=TokenSchemas, summary="商户登录")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    item = schemas.UserLogin(**{'name': form_data.username, 'password': form_data.password})
    return crud.login_user_swagger(db=db, item=item)


@router_user.delete("/delete/{item_id}", summary="删除商户")
@web_try()
@sxtimeit
def delete_user(item_id: int, db: Session = Depends(get_db),):
                # user=Depends(check_admin)):
    return crud.delete_user(item_id=item_id, db=db)


@router_user.put("/{item_id}", summary="更新商户信息")
@web_try()
@sxtimeit
def update_user(item_id: int, update_item: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, item_id=item_id, update_item=update_item)


@router_user.get("/", summary="获取商户列表")
@web_try()
@sxtimeit
def get_users(get_item: schemas.UserGet = Depends(), params: Params = Depends(), db: Session = Depends(get_db),):
              # user=Depends(check_admin)):
    return paginate(crud.get_users(db, get_item), params)


@router_user.get("/getOnce/{item_id}", summary="获取商户信息")
@web_try()
@sxtimeit
def get_user_once(item_id: int, db: Session = Depends(get_db),):
                  # user=Depends(check_admin)):
    return crud.get_user_once(db=db, item_id=item_id)


@router_user.get("/{token}/user_id", summary="获取商户信息")
@web_try()
@sxtimeit
def get_user_id(token: str, db: Session = Depends(get_db)):
    return check_user_id(token, db)


