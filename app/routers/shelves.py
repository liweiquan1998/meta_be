from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit
from fastapi import Depends
from fastapi import APIRouter

router_shelves = APIRouter(
    prefix="/shelves",
    tags=["shelves-货架管理"],
)


@router_shelves.post("/shelf", summary="创建货架")
@web_try()
@sxtimeit
def add_shelves(item: schemas.ShelvesCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_shelves(db=db, item=item)


@router_shelves.get("/{scene_id}", summary="获取货架信息")
@web_try()
@sxtimeit
def get_shelves_once(scene_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_shelves_once(db=db, item_id=scene_id)


@router_shelves.get("", summary="获取货架列表")
@web_try()
@sxtimeit
def get_shelves(params: Params = Depends(), db: Session = Depends(get_db),user=Depends(check_user)):
    return paginate(crud.get_shelves_all(db), params)


@router_shelves.put("/{scene_id}", summary="更新货架信息")
@web_try()
@sxtimeit
def update_shelves(scene_id: int, update_item: schemas.ShelvesUpdate, db: Session = Depends(get_db),
                   user=Depends(check_user)):
    return crud.update_shelves(db=db, item_id=scene_id, update_item=update_item)
