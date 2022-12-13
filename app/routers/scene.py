from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_scene = APIRouter(
    prefix="/scenes",
    tags=["scenes-场景管理"],
)


@router_scene.post("/scene", summary="创建场景")
@web_try()
@sxtimeit
def add_scene(item: schemas.SceneCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_scene(db=db, item=item)


@router_scene.delete("/{scene_id}", summary="删除场景")
@web_try()
@sxtimeit
def delete_scene(scene_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_scene(db=db, item_id=scene_id)


@router_scene.put("/{scene_id}", summary="更新场景信息")
@web_try()
@sxtimeit
def update_scene(scene_id: int, update_item: schemas.SceneUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_scene(db=db, item_id=scene_id, update_item=update_item)


@router_scene.get("", summary="获取场景列表")
@web_try()
@sxtimeit
def get_scenes(get_item: schemas.SceneGet = Depends(), params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_scenes(db, get_item, user), params)


@router_scene.get("/{scene_id}", summary="获取场景信息")
@web_try()
@sxtimeit
def get_scene_once(scene_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_scene_once(db=db, item_id=scene_id)


