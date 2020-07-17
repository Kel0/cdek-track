import json
import re
import time
from typing import Union

import requests
from loguru import logger


class Tracker:
    def __init__(self, track_code: Union[str, int]) -> None:
        self.track_code = self.__parse_code(track_code=track_code)
        self.cookie = self.__init_cookies()
        self.ua = (
            "Mozilla/5.0 (X11; Linux x86_64)"
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        )

    def __init_cookies(self) -> str:
        with open("cookies.txt", "r") as file:
            cookies: list = [
                json.loads(element)["cookie"] for element in file.readlines()
            ]

        return cookies[-1].strip()[:-1]

    def __parse_code(self, track_code: Union[str, int]) -> int:
        if isinstance(track_code, str):
            track_code_re = re.findall("(\d+)", track_code)  # type: ignore

            if len(track_code_re) > 0:
                return int(track_code_re[0])
            else:
                raise Exception("Invalid track code")
        else:
            return track_code

    def __init_link(self) -> str:
        now_time_ml: int = int(time.time()) * 1000
        base_url: str = f"https://cdek.kz/ajax.php?JsHttpRequest={now_time_ml + 2}-xml"

        return base_url

    def __init_headers(self) -> tuple:
        headers = {"accept": "*/*", "cookie": self.cookie, "user-agent": self.ua}
        body: str = f"Action=GetTrackingInfo&invoice={self.track_code}&reqtkn=45d75827d417b7faff8385a4fc36b3ce"
        return headers, body

    @logger.catch
    def track(self) -> dict:
        track_url: str = self.__init_link()
        headers, data = self.__init_headers()

        with requests.Session() as session:
            response: requests.Response = session.post(
                track_url, headers=headers, data=data
            )

        return response.json()
