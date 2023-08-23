import aiohttp
from dataclasses import dataclass

from .const import MODEL_DETAIL, DEFAULT_TIMEOUT
from .exceptions import NotAuthorizedException, NetworkException
from .typing import DeviceInfo, OperationInfo

@dataclass
class YardianDeviceState:
    """Data retrieved from a Yardian device."""

    zones: list[list]
    active_zones: set[int]

class AsyncYardianClient:
    def __init__(
        self, websession: aiohttp.ClientSession, host: str, token: str
    ) -> None:
        self._websession = websession
        self._base_url = f"http://{host}:880"
        self._base_header = {
            "Yardian-Token": token
        }
        self._device_info = None

    async def fetch_oper_info(self) -> OperationInfo:
        try:
            resp = await (
                await self._websession.request(
                    "GET",
                    f"{self._base_url}/API_MGR_GET_OPERINFO",
                    headers=self._base_header,
                    timeout=DEFAULT_TIMEOUT,
                )
            ).json()
        except:
            raise NetworkException()
        else:
            iCode = resp.get("iCode", 0)
            if iCode == 0:
                return resp["result"]
            elif iCode == -1000:
                raise NotAuthorizedException()
            else:
                raise Exception()


    async def fetch_device_info(self) -> DeviceInfo:
        try:
            resp = await (
                await self._websession.request(
                    "GET",
                    f"{self._base_url}/API_GET_DEVICEINFO",
                    headers=self._base_header,
                    timeout=DEFAULT_TIMEOUT,
                )
            ).json()
        except:
            raise NetworkException()
        else:
            iCode = resp.get("iCode", 0)
            if iCode == 0:
                return resp | MODEL_DETAIL[resp["model"]]
            elif iCode == -1000:
                raise NotAuthorizedException()
            else:
                raise Exception()


    async def fetch_active_zones(self):
        try:
            resp = await (
                await self._websession.request(
                    "GET",
                    f"{self._base_url}/API_ZONE_GET_OPENINGZONE",
                    headers=self._base_header,
                    timeout=DEFAULT_TIMEOUT,
                )
            ).json()
        except:
            raise NetworkException()
        else:
            iCode = resp.get("iCode", 0)
            if iCode == 0:
                return resp["result"]
            elif iCode == -1000:
                raise NotAuthorizedException()
            else:
                raise Exception()


    async def fetch_zone_info(self, amount=8):
        oper_info = await self.fetch_oper_info()
        return oper_info["zones"][:amount]

    async def fetch_device_state(self):
        if not self._device_info:
            self._device_info = await self.fetch_device_info()
        zones = await self.fetch_zone_info(self._device_info['zones'])
        active_zones = await self.fetch_active_zones()
        return YardianDeviceState(zones=zones, active_zones=active_zones)

    async def start_irrigation(self, zone_id, duration):
        body = {
            "sEvent": "AE_IRR_START_INST",
            "sPayload": f"[[-1, 0, 0, {zone_id}, {duration * 60}]]",
        }
        await self._websession.request(
            "POST", self._base_url, headers=self._base_header, json=body, timeout=DEFAULT_TIMEOUT
        )

    async def stop_irrigation(self):
        body = {
            "sEvent": "AE_IRR_STOP_TASK",
        }
        await self._websession.request(
            "POST", self._base_url, headers=self._base_header, json=body, timeout=DEFAULT_TIMEOUT
        )
