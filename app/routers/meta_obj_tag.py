from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_meta_obj_tag = APIRouter(
    prefix="/meta_obj_tag",
    tags=["meta_obj_tag-元对象标签管理"],
)


@router_meta_obj_tag.get('/get', summary='获取元对象标签列表')
@web_try()
@sxtimeit
def get_meta_obj_tag(db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_meta_obj_tag(db)


@router_meta_obj_tag.delete('/delete/{item_id}', summary='删除元对象标签')
@web_try()
@sxtimeit
def delete_meta_obj_tag(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_meta_obj_tag(db=db, item_id=item_id)
