from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit
from fastapi import Depends, File, UploadFile, Form
from fastapi import APIRouter, BackgroundTasks

router_marketing_content = APIRouter(
    prefix="/marketing_contents",
    tags=["marketing_contents-营销内容管理"],
)


@router_marketing_content.post("/marketing_content", summary="创建营销内容", )
@web_try()
@sxtimeit
def add_marketing_content(item: schemas.MarketingContentCreate, background_tasks: BackgroundTasks,
                          db: Session = Depends(get_db),
                          user=Depends(check_user)):
    return crud.create_marketing_content(db=db, item=item, creator_id=user.id, background_tasks=background_tasks)


@router_marketing_content.post("/market_minio_content", summary="文件上传minio并更新数据", )
@web_try()
@sxtimeit
def upload_minio_content(file: UploadFile = File(...), params: str = Form(...), db: Session = Depends(get_db)):
    # , user=Depends(check_user)):
    return crud.market_file_content(file=file, params=params, db=db)


@router_marketing_content.post('/compose_video', summary="合成视频")
@web_try()
@sxtimeit
def compose_video(item: schemas.ComposeVideo, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.compose_video(db=db, item=item)


@router_marketing_content.delete("/{content_id}", summary="删除营销内容")
@web_try()
@sxtimeit
def delete_marketing_content(content_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_marketing_content(item_id=content_id, db=db)


@router_marketing_content.put("/{content_id}", summary="更新营销内容信息")
@web_try()
@sxtimeit
def update_marketing_content(content_id: int, update_item: schemas.MarketingContentUpdate,
                             db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_marketing_content(db=db, item_id=content_id, update_item=update_item)


@router_marketing_content.put("/{workspace}/workspace", summary="更新营销内容信息 by workspace")
@web_try()
@sxtimeit
def update_marketing_content_by_workspace(workspace: str, update_item: schemas.MarketingContentUpdate,
                                          db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_marketing_content_by_workspace(db=db, workspace=workspace, update_item=update_item)


@router_marketing_content.get("", summary="获取营销内容列表")
@web_try()
@sxtimeit
def get_marketing_contents(get_item: schemas.MarketingContentGet = Depends(), params: Params = Depends(),
                           db: Session = Depends(get_db), user=Depends(check_user)):
    if not get_item.creator_id:
        get_item.creator_id = user.id
    return paginate(crud.get_marketing_contents(db, get_item), params)


@router_marketing_content.get("/{content_id}", summary="获取营销内容信息")
@web_try()
@sxtimeit
def get_marketing_content_once(content_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_marketing_content_once(db=db, item_id=content_id)
