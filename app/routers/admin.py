from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from utils import web_try, sxtimeit
from app.common.validation import *

router_admin = APIRouter(
    prefix="/admin",
    tags=["admin-超级管理员"],
)


@router_admin.post("/create", summary="创建超级管理员")
@web_try()
@sxtimeit
def add_admin(item: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db=db, item=item)


@router_admin.post("/login_fastapi", response_model=TokenSchemas, summary="fastapi超级管理员登录")
def login_admin_api(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    item = schemas.AdminLogin(**{'name': form_data.name, 'password': form_data.password})
    return crud.login_admin_api(db=db, item=item)


@router_admin.post("/login", summary="超级管理员登录")
@web_try()
@sxtimeit
def login_admin(item: schemas.AdminLogin, db: Session = Depends(get_db)):
    return crud.login_admin(db=db, item=item)


@router_admin.delete('/delete/{id}', summary="删除超级管理员")
@web_try()
@sxtimeit
def delete_admin(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_admin(item_id=item_id, db=db)

#
# @router_admin.put("/{item_id}", summary="更新超级管理员信息")
# @web_try()
# @sxtimeit
# def update_admin(item_id: int, update_item: schemas.AdminUpdate, db: Session = Depends(get_db)):
#     return crud.update_admin(db=db, item_id=item_id, update_item=update_item)
#
#
# @router_admin.get("/", summary="获取超级管理员列表")
# @web_try()
# @sxtimeit
# def get_admins(get_item: schemas.AdminGet = Depends(), params: Params = Depends(), db: Session = Depends(get_db)):
#     return paginate(crud.get_admins(db, get_item), params)
#
#
# @router_admin.get("/getOnce/{item_id}", summary="获取超级管理员信息")
# @web_try()
# @sxtimeit
# def get_admin_once(item_id: int, db: Session = Depends(get_db)):
#     return crud.get_admin_once(db=db, item_id=item_id)
