from fastapi import APIRouter, Depends
from app.handler import logistics_company
from utils import web_try, sxtimeit

router_logistics = APIRouter(
    prefix="/logistics",
    tags=["logistics-物流管理"],
)

@router_logistics.get("/")
@web_try()
@sxtimeit
def get_logistics():
    return logistics_company.logistics_company_list



