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
    RENEW_TOKEN = 'Renew-Token'
    AUTH_API = 'Auth-Api'

class EliteCloudSection(StrEnum):
    STATUS = 'status'
    AREA = 'area'
    INPUT = 'input'
    OUTPUT = 'output'
    TAMPER = 'tamper'
    SYSTEM = 'system'

class EliteCloudCmdSection(StrEnum):
    STAY = "stay"
    ARM = "arm"
    INPUT = 'input'
    OUTPUT = 'output'

class EliteCloudCmdAction(StrEnum):
    TOGGLE = 'toggle'

class EliteCloudStatusType(StrEnum):
    MAINS_FAIL  = "mains fail"
    BATTERY_LOW = "battery low"     

ELITE_CLOUD_STATUS_TYPES_TAMPER = [
    EliteCloudStatusType.MAINS_FAIL,
    EliteCloudStatusType.BATTERY_LOW,
]
ELITE_CLOUD_STATUS_TYPES_SYSTEM = [
]

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

class EliteCloudSites(list[EliteCloudSite]):
    def find_by_uuid(self, uuid: str):
        return next( (s for s in self if s.uuid==uuid), None)

    def get_by_uuid(self, uuid: str):
        site = self.find_by_uuid(uuid)
        if site is None:
            raise EliteCloudParamError(f"No site found with id '{uuid}'")
        return site

    def get_by_mac(self, mac: str):
        site = next( (s for s in self if s.panel_mac==mac), None)
        if site is None:
            raise EliteCloudParamError(f"No site found with mac '{mac}'")
        return site
    
    def get_by_serial(self, serial: str):
        site = next( (s for s in self if s.panel_serial==serial), None)
        if site is None:
            raise EliteCloudParamError(f"No site found with serial '{serial}'")
        return site

