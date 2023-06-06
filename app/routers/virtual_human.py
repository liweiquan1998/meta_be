from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit
from fastapi import Depends
from fastapi import APIRouter

router_virtual_humans = APIRouter(
    prefix="/virtual_humans",
    tags=["virtual_humans-虚拟人管理"],
)


@router_virtual_humans.post("/check_name", summary="校验虚拟人名称是否重复")
@web_try()
@sxtimeit
def check_virtual_human_name(item: schemas.VirtualHumanCheckName, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.check_virtual_human_name(db=db, item=item, user=user)

@router_virtual_humans.post("/virtual_human", summary="创建虚拟人")
@web_try()
@sxtimeit
def add_virtual_human(item: schemas.VirtualHumanCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_virtual_human(db=db, item=item, user=user)


@router_virtual_humans.delete("/{item_id}", summary="删除虚拟人")
@web_try()
@sxtimeit
def delete_virtual_human(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_virtual_human(item_id=item_id, db=db, user=user)


@router_virtual_humans.put("/{item_id}", summary="更新虚拟人信息")
@web_try()
@sxtimeit
def update_virtual_human(item_id: int, update_item: schemas.VirtualHumanUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_virtual_human(db=db, item_id=item_id, update_item=update_item,user=user)


@router_virtual_humans.get("", summary="获取虚拟人列表")
@web_try()
@sxtimeit
def get_virtual_humans(get_item: schemas.VirtualHumanGet = Depends(), params: Params = Depends(),
                       db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_virtual_humans(db, get_item, user), params)


@router_virtual_humans.get("/{item_id}", summary="获取虚拟人信息")
@web_try()
@sxtimeit
def get_virtual_human_once(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_virtual_human_once(db=db, item_id=item_id)


@router_virtual_humans.get("/{creator_id}/creator_id", summary="由创建者id->获取虚拟人信息")
@web_try()
@sxtimeit
def get_virtual_human_once(creator_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_virtual_human_once_by_creator_id(db=db, creator_id=creator_id)

