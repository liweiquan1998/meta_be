from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter

router_meta_obj_tag = APIRouter(
    prefix="/meta_obj_tags",
    tags=["meta_obj_tags-元对象标签管理"],
)


@router_meta_obj_tag.get('', summary='获取元对象标签列表')
@web_try()
@sxtimeit
def get_meta_obj_tag(db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_meta_obj_tag(db)


@router_meta_obj_tag.delete('/{tag_id}', summary='删除元对象标签')
@web_try()
@sxtimeit
def delete_meta_obj_tag(tag_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_meta_obj_tag(db=db, item_id=tag_id)


@router_meta_obj_tag.get("/all", summary="拿到所有元对象")
@web_try()
@sxtimeit
def get_meta_objs(db: Session = Depends(get_db), params: Params = Depends()):
    return paginate(crud.get_meta_all(db), params)
