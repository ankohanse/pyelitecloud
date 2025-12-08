from datetime import datetime
import logging

from dataclasses import dataclass
from enum import Enum, StrEnum

from .const import (
    CALL_CONTEXT_SYNC,
    CALL_CONTEXT_ASYNC,
)

_LOGGER = logging.getLogger(__name__)


class CallContext(StrEnum):
    SYNC = CALL_CONTEXT_SYNC
    ASYNC = CALL_CONTEXT_ASYNC

class LoginMethod(StrEnum):
    ACCESS_TOKEN = 'Access-Token'
    REFRESH_TOKEN = 'Refresh-Token'
    AUTH_API = 'Auth-Api'



class EliteCloudError(Exception):
    """Exception to indicate generic error failure."""    
    
class EliteCloudConnectError(EliteCloudError):
    """Exception to indicate authentication failure."""

class EliteCloudAuthError(EliteCloudError):
    """Exception to indicate authentication or authorization failure."""

class EliteCloudDataError(EliteCloudError):
    """Exception to indicate generic data failure."""  

class EliteCloudParamError(EliteCloudError):
    """Exception to indicate invalid parameter was passed."""


@dataclass
class EliteCloudSite:
    uuid: str
    name: str
    panel_mac: str
    panel_serial: str


@dataclass
class EliteCloudHistoryItem:
    dt: datetime
    op: str
    rsp: str|None = None
 
    @staticmethod
    def create(dt: datetime, context: str , request: dict|None, response: dict|None, token: dict|None) -> 'EliteCloudHistoryItem':
        item = EliteCloudHistoryItem( 
            dt = dt, 
            op = context,
        )

        # If possible, add a summary of the response status and json res and code
        if response:
            rsp_parts = []
            if "status_code" in response:
                rsp_parts.append(response["status_code"])
            if "status" in response:
                rsp_parts.append(response["status"])
            
            item.rsp = ', '.join(rsp_parts)

        return item


@dataclass
class EliteCloudHistoryDetail:
    dt: datetime
    req: dict|None
    rsp: dict|None
    token: dict|None

    @staticmethod
    def create(dt: datetime, context: str , request: dict|None, response: dict|None, token: dict|None) -> 'EliteCloudHistoryDetail':
        detail = EliteCloudHistoryDetail(
            dt = dt, 
            req = request,
            rsp = response,
            token = token,
        )
        return detail


class EliteCloudDictFactory:
    @staticmethod
    def exclude_none_values(x):
        """
        Usage:
          item = EliteCloudHistoryItem(...)
          item_as_dict = asdict(item, dict_factory=EliteCloudDictFactory.exclude_none_values)
        """
        return { k: v for (k, v) in x if v is not None }

