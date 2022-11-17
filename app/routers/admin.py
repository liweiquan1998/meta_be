from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from utils import web_try, sxtimeit

router_admin = APIRouter(
    prefix="/admin",
    tags=["admin-超级管理员"],
)


@router_admin.get("/")
@web_try()
@sxtimeit
def get_admins(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_admins(db), params)


@router_admin.get("/getOnce/{item_id}")
@web_try()
@sxtimeit
def get_admin_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_admin_once(db=db, item_id=item_id)


@router_admin.put("/{item_id}")
@web_try()
@sxtimeit
def update_admin(item_id: int, update_item: schemas.AdminUpdate, db: Session = Depends(get_db)):
    return crud.update_admin(db=db, item_id=item_id, update_item=update_item)


@router_admin.post("/create")
@web_try()
@sxtimeit
def add_admin(item: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db=db, item=item)
