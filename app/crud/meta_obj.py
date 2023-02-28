import os.path
import threading
import time
import cv2
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *
from app.crud.meta_obj_tag import create_meta_obj_tag
from utils.valid_name import is_valid_name
from app.crud.aigc import *
from app.crud.user import *
from app.crud.file import *


def meta_obj_add_username(mo, db: Session, ):
    if type(mo) == list:
        res = [r.to_dict() for r in mo]
        for m in res:
            try:
                m['creator_name'] = db.query(models.User).filter(models.User.id == m['creator_id']).first().name
            except Exception as e:
                raise Exception(f"meta_obj {m['id']} 的创建者不存在")
    else:
        res = mo.to_dict()
        res['creator_name'] = db.query(models.User).filter(models.User.id == res['creator_id']).first().name
    return res


def create_meta_obj(db: Session, item, creator_id, upload_type=None):
    # sourcery skip: use-named-expression
    def db_save(_item, more_dict):
        _db_item = models.MetaObj(**item.dict(), **more_dict)
        max_id_row = db.execute('select max(id) from public.meta_obj').fetchone()
        if max_id_row:
            max_id = max_id_row[0]
            _db_item.id = max_id + 1
        db.add(_db_item)
        try:
            db.commit()
        except Exception as e:
            print('#####################', e)
            raise e
        db.refresh(_db_item)
        return _db_item

    def minio2nfs(minio_p):
        file_byte = get_minio_file_byte(minio_p.split('minio/')[-1])
        yearmonth = time.strftime("%Y%m", time.localtime())
        if not os.path.exists(f"/mnt/nfs/SceneAssets/{yearmonth}"):
            os.mkdir(f"/mnt/nfs/SceneAssets/{yearmonth}")
        nfs_p = f"/mnt/nfs/SceneAssets/{yearmonth}/{minio_p.split('/')[-1]}"
        with open(nfs_p, "wb") as f:
            f.write(file_byte)
        return '/file/' + nfs_p

    def video_fist_frame(video_p):
        root_p = Path(f"{minio2nfs(video_p)}")
        print(root_p)
        vidcap = cv2.VideoCapture(str(root_p))
        success, image = vidcap.read()
        n = 1
        while n < 30:
            success, image = vidcap.read()
            n += 1
        thumbnail_path = str(root_p.parent / f"{uuid.uuid1()}.png")
        print(thumbnail_path)
        imag = cv2.imwrite(thumbnail_path, image)
        if imag:
            return thumbnail_path
        else:
            raise Exception('视频转换缩略图失败')

    def model_save(_item):
        # 补充字段
        _model_dict = {
            'create_time': int(time.time()),
            'creator_id': creator_id,
            'status': 1,
        }
        # 存入数据库
        _db_item = db_save(_item, _model_dict)
        return _db_item

    # 重复名称检查
    item.name = is_valid_name(item.name, 10)
    res: models.MetaObj = db.query(models.MetaObj).filter(models.MetaObj.name == item.name,
                                                          models.MetaObj.creator_id == creator_id).first()
    if res:
        raise Exception(f"物品 {item.name} 已存在")

    # 商品
    if item.kind == 1:
        # 模型上传
        if item.type == 1:
            db_item = model_save(item)
        # 图片生成
        elif item.type == 0:  # todo 要改
            # 取出缩略图
            nfs_path = minio2nfs(item.aigc[0])
            item.thumbnail = nfs_path  # todo
            # 补充字段
            image_dict = {
                'create_time': int(time.time()),
                'creator_id': creator_id,
                'status': 0,
            }
            # 存入数据库
            db_item = db_save(item, image_dict)
            # 向算法端发送请求
            threading.Thread(target=send_nerf_request, args=(item.aigc, db_item.id, 'image')).start()
        # 视频生成
        elif item.type == 2:
            # 取出缩略图
            nfs_path = video_fist_frame(item.aigc[0])
            item.thumbnail = nfs_path
            # 补充字段
            video_dict = {
                'create_time': int(time.time()),
                'creator_id': creator_id,
                'status': 0,
                'thumbnail': nfs_path
            }
            # 存入数据库
            db_item = db_save(item, video_dict)
            # 向算法端发送请求
            threading.Thread(target=send_nerf_request, args=(item.aigc, db_item.id, 'video')).start()
        else:
            raise Exception('type参数错误 应为0: 上传模型 ,1: 图片生成,2: 视频生成')
    # 场景素材
    elif item.kind == 0:
        # tag处理
        create_meta_obj_tag(db, item.tag)
        # 保存模型
        db_item = model_save(item)
    else:
        raise Exception("meta_obj 种类(kind)不合法 应为 0: 场景素材 1: 商品 ")

    return db_item


def update_meta_obj(db: Session, item_id: int, update_item: schemas.MetaObjUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.MetaObj)


def get_meta_obj_once(db: Session, item_id: int):
    res: models.MetaObj = db.query(models.MetaObj).filter(models.MetaObj.id == item_id).first()
    if res.aigc:
        res.aigc = res.aigc.replace('{', '').replace('}', '').split(',')
    return meta_obj_add_username(res, db)


def get_meta_obj_by_creator_id(db: Session, creator_id: int):
    meta_objs = db.query(models.MetaObj).filter(models.MetaObj.creator_id == creator_id).all()
    return meta_obj_add_username(meta_objs, db)


def get_meta_objs(db: Session, item: schemas.MetaObjGet):
    # sourcery skip: inline-immediately-returned-variable
    db_query = db.query(models.MetaObj)
    if item.name and item.name != "":
        db_query = db_query.filter(models.MetaObj.name.like(f"%{item.name}%"))
    if item.kind is not None and item.kind != -1:
        db_query = db_query.filter(models.MetaObj.kind == item.kind)
    if item.type is not None and item.type != -1:
        db_query = db_query.filter(models.MetaObj.type == item.type)
    if item.status is not None and item.status != -1:
        db_query = db_query.filter(models.MetaObj.status == item.status)
    if item.create_time is not None and item.create_time != -1:
        db_query = db_query.filter(models.MetaObj.create_time <= item.create_time + 86400)
        db_query = db_query.filter(models.MetaObj.create_time >= item.create_time)
    if item.tag is not None and item.tag != "":
        db_query = db_query.filter(models.MetaObj.tag == item.tag)
    if item.creator_id is not None and item.creator_id != -1:
        db_query = db_query.filter(models.MetaObj.creator_id == item.creator_id)

    meta_objs = db_query.all()
    for mo in meta_objs:
        if mo.aigc:
            mo.aigc = mo.aigc.replace('{', '').replace('}', '').split(',')
    return meta_obj_add_username(meta_objs, db)


def delete_meta_obj(db: Session, item_id: int):
    item = db.query(models.MetaObj).filter(models.MetaObj.id == item_id).first()
    if not item:
        raise Exception(f"meta_obj {item_id} 不存在")
    db.delete(item)
    db.commit()
    db.flush()
    return True


def upload_update_meta(file, params: str, db: Session):
    file_byte = file.file.read()
    file_name = f'{uuid.uuid1()}{Path(file.filename).suffix}'
    result = Path('SceneAssets') / f'{time.strftime("%Y%m", time.localtime())}'
    sys_path = '/mnt/nfs/' / result
    sys_path.mkdir(parents=True, exist_ok=True)
    real_path = sys_path / file_name
    try:
        with real_path.open('wb') as f:
            f.write(file_byte)
        real_path.chmod(0o777)
        uri = f'/file/nfs/{str(result / file_name)}'
    except Exception as e:
        raise Exception(400, f"上传失败{e}")
    params = eval(params)
    item_id = params.get("mo_id")
    db_item = db.query(models.MetaObj).filter(models.MetaObj.id == item_id).first()
    if not db_item:
        raise Exception('未找到该任务')
    db_item.status = 1
    db_item.thumbnail = uri
    db.commit()
    db.flush()
    db.refresh(db_item)
    return db_item

