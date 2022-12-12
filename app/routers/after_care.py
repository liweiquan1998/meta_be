from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app.common.validation import check_user
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time


router_after_care = APIRouter(
    prefix="/after_cares",
    tags=["after_cares-售后管理"],
)



@router_after_care.get("")
@web_try()
@sxtimeit
def get_after_cares(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_after_cares(db), params)


@router_after_care.get("/{after_care_id}")
@web_try()
@sxtimeit
def get_after_care_once(after_care_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_after_care_once_dict(db=db, item_id=after_care_id)


@router_after_care.put("/{after_care_id}")
@web_try()
@sxtimeit
def update_after_care(after_care_id: int, update_item: schemas.AfterCareUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_after_care(db=db, item_id=after_care_id, update_item=update_item)


@router_after_care.delete("/{after_care_id}")
@web_try()
@sxtimeit
def delete_after_care(after_care_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_after_care(db=db,item_id=after_care_id)



