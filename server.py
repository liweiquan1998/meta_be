from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import Base, engine
from app.routers.customer import router_customer
from app.routers.user import router_user
from app.routers.admin import router_admin
from app.routers.product import router_product
from app.routers.sku import router_sku
from app.routers.order import router_order
from app.routers.logistics import router_logistics
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
app.include_router(router_customer)
app.include_router(router_user)
app.include_router(router_admin)
app.include_router(router_product)
app.include_router(router_sku)
app.include_router(router_order)
app.include_router(router_logistics)



# Get 健康检查
@app.get("/jpt/ping", description="健康检查")
def ping():
    return "pong!!"
