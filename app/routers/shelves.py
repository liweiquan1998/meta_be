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


@router_shelves.get("/{shelf_id}", summary="获取一个货架信息")
@web_try()
@sxtimeit
def get_shelves_once(shelf_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_shelves_once(db=db, item_id=shelf_id)


@router_shelves.get("/scene/{scene_id}", summary="获取一个场景下的货架列表")
@web_try()
@sxtimeit
def get_shelves(scene_id: int, params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_shelves_all_scene(db, scene_id), params)


@router_shelves.put("/{shelf_id}", summary="更新货架信息")
@web_try()
@sxtimeit
def update_shelves(shelf_id: int, update_item: schemas.ShelvesUpdate, db: Session = Depends(get_db),
                   user=Depends(check_user)):
    return crud.update_shelves(db=db, item_id=shelf_id, update_item=update_item)
