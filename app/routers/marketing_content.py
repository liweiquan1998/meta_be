from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_marketing_content = APIRouter(
    prefix="/marketing_content",
    tags=["marketing_content-营销内容管理"],
)


@router_marketing_content.post("/", summary="创建营销内容", )
@web_try()
@sxtimeit
def add_marketing_content(item: schemas.MarketingContentCreate, db: Session = Depends(get_db)):
    return crud.create_marketing_content(db=db, item=item)


@router_marketing_content.post('/compose_video', summary="合成视频")
@web_try()
@sxtimeit
def compose_video(item: schemas.ComposeVideo, db: Session = Depends(get_db)):
    return crud.compose_video(db=db, item=item)


@router_marketing_content.delete("/{item_id}", summary="删除营销内容")
@web_try()
@sxtimeit
def delete_marketing_content(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_marketing_content(item_id=item_id, db=db)


@router_marketing_content.put("/{item_id}", summary="更新营销内容信息")
@web_try()
@sxtimeit
def update_marketing_content(item_id: int, update_item: schemas.MarketingContentUpdate, db: Session = Depends(get_db)):
    return crud.update_marketing_content(db=db, item_id=item_id, update_item=update_item)


@router_marketing_content.put("/{workspace}/workspace", summary="更新营销内容信息 by workspace")
@web_try()
@sxtimeit
def update_marketing_content_by_workspace(workspace: str, update_item: schemas.MarketingContentUpdate,
                                          db: Session = Depends(get_db)):
    return crud.update_marketing_content_by_workspace(db=db, workspace=workspace, update_item=update_item)


@router_marketing_content.get("/", summary="获取营销内容列表")
@web_try()
@sxtimeit
def get_marketing_contents(get_item: schemas.MarketingContentGet = Depends(), params: Params = Depends(),
                           db: Session = Depends(get_db)):
    return paginate(crud.get_marketing_contents(db, get_item), params)


@router_marketing_content.get("/{item_id}", summary="获取营销内容信息")
@web_try()
@sxtimeit
def get_marketing_content_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_marketing_content_once(db=db, item_id=item_id)