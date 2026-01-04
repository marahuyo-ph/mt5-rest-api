from enum import Enum
from pydantic import BaseModel, model_validator, ConfigDict

class ErrorCodes(Enum):
    RES_S_OK = 1
    RES_E_FAIL = -1
    RES_E_INVALID_PARAMS = -2
    RES_E_NO_MEMORY = -3
    RES_E_NOT_FOUND = -4
    RES_E_INVALID_VERSION = -5
    RES_E_AUTH_FAILED = -6
    RES_E_UNSUPPORTED = -7
    RES_E_AUTO_TRADING_DISABLED = -8
    RES_E_INTERNAL_FAIL = -10000
    RES_E_INTERNAL_FAIL_SEND = -10001
    RES_E_INTERNAL_FAIL_RECEIVE = -10002
    RES_E_INTERNAL_FAIL_INIT = -10003
    RES_E_INTERNAL_FAIL_CONNECT = -10003
    RES_E_INTERNAL_FAIL_TIMEOUT = -10005


class ErrorResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=False)
    code: ErrorCodes
    message: str
    
    @model_validator(mode='before')
    def convert_tuple(cls, data):
        if isinstance(data, tuple):
            return {'code': data[0], 'message': data[1]}
        return data
