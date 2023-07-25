import aiohttp

from .const import MODEL_DETAIL, DEFAULT_TIMEOUT

class AsyncYardianClient:
    def __init__(
        self, websession: aiohttp.ClientSession, host: str, token: str
    ) -> None:
        self._websession = websession
        self._base_url = f"http://{host}:880"
        self._base_header = {
            "Yardian-Token": token
        }

    async def fetch_oper_info(self):
        resp = await (
            await self._websession.request(
                "GET",
                f"{self._base_url}/API_MGR_GET_OPERINFO",
                headers=self._base_header,
                timeout=DEFAULT_TIMEOUT,
            )
        ).json()

        if "iCode" in resp and resp["iCode"] != 0:
            raise Exception()

        return resp["result"]

    async def fetch_device_info(self):
        resp = await (
            await self._websession.request(
                "GET",
                f"{self._base_url}/API_GET_DEVICEINFO",
                headers=self._base_header,
                timeout=DEFAULT_TIMEOUT,
            )
        ).json()

        if "iCode" in resp and resp["iCode"] != 0:
            raise Exception()

        return resp | MODEL_DETAIL[resp["model"]]

    async def fetch_active_zones(self):
        resp = await (
            await self._websession.request(
                "GET",
                f"{self._base_url}/API_ZONE_GET_OPENINGZONE",
                headers=self._base_header,
                timeout=DEFAULT_TIMEOUT,
            )
        ).json()

        if "iCode" in resp and resp["iCode"] != 0:
            raise Exception()

        return resp["result"]

    async def fetch_zone_info(self, amount=8):
        oper_info = await self.fetch_oper_info()
        return oper_info["zones"][:amount]

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
