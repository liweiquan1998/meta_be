from fastapi_pagination import Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter


router_scene_base = APIRouter(
    prefix="/scene_bases",
    tags=["scene_bases-基础场景"],
)


@router_scene_base.get("", summary="获取模版场景列表")
@web_try()
@sxtimeit
def get_scene_bases(get_item: schemas.SceneBaseGet = Depends(), params: Params = Depends(),
                    db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_scene_base(db, get_item)


@router_scene_base.get("/{scene_id}", summary="获取模版场景信息")
@web_try()
@sxtimeit
def get_scene_base_once(scene_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_scene_base_once(db=db, item_id=scene_id)
