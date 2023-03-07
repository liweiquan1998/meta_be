from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends, UploadFile, File, Form
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_meta_obj = APIRouter(
    prefix="/meta_objs",
    tags=["meta_objs-元对象管理"],
)


@router_meta_obj.post("/meta_obj", summary="创建元对象")
@web_try()
@sxtimeit
def add_meta_obj_create(item: schemas.MetaObjCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_meta_obj(db=db, item=item, creator_id=user.id)


@router_meta_obj.post("/meta_nerf_content", summary="上传文件并更新数据")
@web_try()
@sxtimeit
def meta_obj_create(file: UploadFile = File(...), params: str = Form(...), db: Session = Depends(get_db)):
    return crud.upload_update_meta(file=file, params=params, db=db)


@router_meta_obj.post("/create_by_images", summary="由图片创建元对象")
@web_try()
@sxtimeit
def add_meta_obj_by_images(item: schemas.MetaObjByImageCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_meta_obj(db=db, item=item, creator_id=user.id, upload_type='image')


@router_meta_obj.post("/create_by_video", summary="由视频创建元对象")
@web_try()
@sxtimeit
def add_meta_obj_by_video(item: schemas.MetaObjByVideoCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_meta_obj(db=db, item=item, creator_id=user.id, upload_type='video')


@router_meta_obj.post("/create_by_model", summary="由模型创建元对象")
@web_try()
@sxtimeit
def add_meta_obj_by_model(item: schemas.MetaObjByModelCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_meta_obj(db=db, item=item, creator_id=user.id)


@router_meta_obj.get("/{item_id}", summary="获取单个元对象信息")
@web_try()
@sxtimeit
def get_meta_obj_once(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_meta_obj_once(db=db, item_id=item_id)


@router_meta_obj.get("/{creator_id}/get_by_creator_id", summary="由创建者id->元对象")
@web_try()
@sxtimeit
def get_meta_obj_by_creator_id(creator_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_meta_obj_by_creator_id(db=db, creator_id=creator_id)


@router_meta_obj.get("", summary="获取元对象列表")
@web_try()
@sxtimeit
def get_meta_objs(get_item: schemas.MetaObjGet = Depends(), params: Params = Depends(),
                  db: Session = Depends(get_db), total: int = 0, user=Depends(check_user)):
    get_item.creator_id = user.id
    if total:
        return crud.get_meta_objs(db, get_item)
    return paginate(crud.get_meta_objs(db, get_item), params)


@router_meta_obj.get("/all", summary="拿到所有元对象")
@sxtimeit
def get_meta_objs(db: Session = Depends(get_db), params: Params = Depends()):
    return paginate(crud.get_meta_all(db), params)


@router_meta_obj.put("/{item_id}", summary="更新元对象状态")
@web_try()
@sxtimeit
def update_meta_obj(item_id: int, update_item: schemas.MetaObjUpdate, db: Session = Depends(get_db),
                    user=Depends(check_user)):
    return crud.update_meta_obj(db=db, item_id=item_id, update_item=update_item)


@router_meta_obj.delete("/{item_id}", summary="删除元对象")
@web_try()
@sxtimeit
def delete_meta_obj(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_meta_obj(db=db, item_id=item_id)
