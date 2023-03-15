from app import schemas, get_db, crud
from utils import web_try, sxtimeit
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.common.validation import check_user

router_marketing_component = APIRouter(
    prefix="/marking_component",
    tags=["marking_component-营销组件内容"],
)


@router_marketing_component.post("/", summary="创建营销组件内容")
@web_try()
@sxtimeit
def add_marking_component(item: schemas.MarketingComponentCreate, db: Session = Depends(get_db),
                          user=Depends(check_user)):
    return crud.create_marketing_component(db=db, item=item)


@router_marketing_component.delete("/{marking_component_id}", summary="删除营销组件内容")
@web_try()
@sxtimeit
def delete_marking_component(marking_component_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_marketing_component(db=db, item_id=marking_component_id)


@router_marketing_component.put("/{marking_component_id}", summary="更新营销组件内容")
@web_try()
@sxtimeit
def update_marking_component(marking_component_id: int, item: schemas.MarketingComponentUpdate,
                             db: Session = Depends(get_db),
                             user=Depends(check_user)):
    return crud.update_marketing_component(db=db, item=item, item_id=marking_component_id)


@router_marketing_component.get("/", summary="获取营销组件内容列表")
@web_try()
@sxtimeit
def get_marking_component(get_item: schemas.MarketingComponentGet = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_marketing_component(item=get_item, db=db)
