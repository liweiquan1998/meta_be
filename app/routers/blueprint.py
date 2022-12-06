from fastapi_pagination import paginate, Params
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *

router_blueprint = APIRouter(
    prefix="/blueprint",
    tags=["blueprint-蓝图管理"],
)


@router_blueprint.post("/", summary="创建蓝图")
@web_try()
@sxtimeit
def add_blueprint(item: schemas.BlueprintCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    blueprint = crud.get_blueprint_once_by_store_id(db, item.store_id)
    if not blueprint:
        item.creator_id = user.id
        return crud.create_blueprint(db=db, item=item)
    else:
        return crud.update_blueprint(db, blueprint.id, schemas.BlueprintUpdate(config_uri=item.config_uri))


@router_blueprint.delete("/{item_id}", summary="删除蓝图")
@web_try()
@sxtimeit
def delete_blueprint(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_blueprint(item_id=item_id, db=db)


@router_blueprint.put("/{item_id}", summary="更新蓝图信息")
@web_try()
@sxtimeit
def update_blueprint(item_id: int, update_item: schemas.BlueprintUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_blueprint(db=db, item_id=item_id, update_item=update_item)


@router_blueprint.get("/{item_id}", summary="获取蓝图信息")
@web_try()
@sxtimeit
def get_blueprint_once(item_id: int, db: Session = Depends(get_db), user=Depends(check_user) ):
    return crud.get_blueprint_once(db=db, item_id=item_id)


@router_blueprint.get("/", summary="获取蓝图列表")
@web_try()
@sxtimeit
def get_blueprints( params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user) ):
    return paginate(crud.get_blueprints(db), params)


