import traceback
import numpy as np
from decorator import decorator
from fastapi.responses import JSONResponse
from fastapi import Depends
from app import get_db
from app.models.database import Session


def json_compatible(data):
    if isinstance(data,dict):
        return {k:json_compatible(v) for k,v in data.items()}
    if isinstance(data,bytes):
        return str(data)
    if isinstance(data,np.ndarray):
        return data.tolist()
    return data

def web_try(exception_ret=None):
    @decorator
    def f(func, *args, **kwargs):
        error_code = 200
        ret = None
        msg = ''
        try:
            session = None
            for arg in args:
                if isinstance(arg, Session):
                    session = arg
            ret = func(*args, **kwargs)
        except Exception as e:
            msg = traceback.format_exc()
            if 'sqlalchemy' in str(msg).lower():
                if session:
                    session.rollback()
                    session.close()
                    msg = 'database-error \n.'
            if len(e.args) > 0 and isinstance(e.args[0], int):
                error_code = e.args[0]
            else:
                error_code = 400
            print('--------------------------------')
            print('Get Exception in web try :( \n{}\n'.format(msg))
            print('--------------------------------')
            if callable(exception_ret):
                ret = exception_ret()
            else:
                ret = exception_ret
        finally:
            if ret is not None and isinstance(ret, JSONResponse):
                return ret
            return json_compatible({"code": error_code,
                                    "data": ret,
                                    "msg": msg.split('\n')[-2] if msg is not '' else msg})
    return f
