from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

router_backgrounds = APIRouter(
    prefix="/backgrounds",
    tags=["backgrounds-背景管理"],
)


@router_backgrounds.post("/", summary="创建背景")
@web_try()
@sxtimeit
def create_background(item: schemas.BackgroundCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_background(db, item)


@router_backgrounds.get("/{background_id}", summary="获取背景")
@web_try()
@sxtimeit
def get_background(background_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_background_once(db, background_id)


@router_backgrounds.get("/", summary="获取背景列表")
@web_try()
@sxtimeit
def get_backgrounds(get_item: schemas.BackgroundGet = Depends(), params: Params = Depends(),
                    db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_backgrounds(db, get_item), params)


@router_backgrounds.put("/{background_id}", summary="更新背景")
@web_try()
@sxtimeit
def update_background(background_id: int, update_item: schemas.BackgroundUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_background(db, background_id, update_item)


@router_backgrounds.delete("/{background_id}", summary="删除背景")
@web_try()
@sxtimeit
def delete_background(background_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_background(db, background_id)
