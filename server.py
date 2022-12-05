from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import Base, engine
from app.routers.customer import router_customer
from app.routers.file import router_file
from app.routers.store import router_store
from app.routers.user import router_user
from app.routers.admin import router_admin
from app.routers.product import router_product
from app.routers.sku import router_sku
from app.routers.scene import router_scene
from app.routers.scene_base import router_scene_base
from app.routers.order import router_order
from app.routers.after_care import router_after_care
from app.routers.meta_obj import router_meta_obj
from app.routers.meta_obj_tag import router_meta_obj_tag
from app.routers.shelves import router_shelves
from app.routers.product_sku import router_product_sku
from app.routers.business import router_businesses
from app.routers.virtual_human import router_virtual_humans
from app.routers.marketing_content import router_marketing_content
from app.routers.live_account import router_live_account
from app.routers.live_streaming import router_live_streaming
from app.routers.background import router_backgrounds
from utils.sx_log import format_print

format_print()
Base.metadata.create_all(bind=engine)
app = FastAPI(docs_url='/meta/docs', redoc_url='/meta/redoc', title="元宇宙电商平台后台")

# CORS 跨源资源共享
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print('server init finish:)!!!')
# app.include_router(router_customer)
app.include_router(router_user)
# app.include_router(router_admin)
app.include_router(router_product)
app.include_router(router_sku)
app.include_router(router_scene)
app.include_router(router_scene_base)
app.include_router(router_order)
app.include_router(router_after_care)
app.include_router(router_meta_obj)
app.include_router(router_meta_obj_tag)
app.include_router(router_shelves)
app.include_router(router_file)
app.include_router(router_product_sku)
app.include_router(router_store)
app.include_router(router_businesses)
app.include_router(router_virtual_humans)
app.include_router(router_marketing_content)
app.include_router(router_live_account)
app.include_router(router_live_streaming)
app.include_router(router_backgrounds)

# Get 健康检查
@app.get("/ping", description="健康检查")
def ping():
    return "pong!!"
