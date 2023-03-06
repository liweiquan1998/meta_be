from fastapi_pagination import paginate, Params
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit
from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *

router_effect = APIRouter(
    prefix="/effects",
    tags=["effects-特效管理"],
)


@router_effect.post("/effect", summary="创建特效")
@web_try()
@sxtimeit
def add_effect(item: schemas.EffectCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_effect(db=db, item=item, user=user)


@router_effect.post("/effect", summary="获取特效列表")
@web_try()
@sxtimeit
def get_effect(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_effect(db=db, user=user), params)


@router_effect.delete("/{item_id}", summary="删除特效")
@web_try()
@sxtimeit
def delete_effect(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_effect(item_id=item_id, db=db)
