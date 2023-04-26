from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

router_background_images = APIRouter(
    prefix="/background_images",
    tags=["background_images-图片视频背景管理"],
)


@router_background_images.post("/", summary="创建图片视频背景")
@web_try()
@sxtimeit
def create_background_images(item: schemas.BackgroundCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_background(db, item)
#
#
# @router_background_images.get("/{background_images_id}", summary="获取图片视频背景")
# @web_try()
# @sxtimeit
# def get_background(background_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
#     return crud.get_background_once(db, background_id)
#
#
# @router_background_images.get("", summary="获取图片视频背景列表")
# @web_try()
# @sxtimeit
# def get_backgrounds(get_item: schemas.BackgroundGet = Depends(), params: Params = Depends(),
#                     db: Session = Depends(get_db), user=Depends(check_user)):
#     return paginate(crud.get_backgrounds(db, get_item), params)
#
#
# @router_background_images.delete("/{background_images_id}", summary="删除图片视频背景")
# @web_try()
# @sxtimeit
# def delete_background(background_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
#     return crud.delete_background(db, background_id)
