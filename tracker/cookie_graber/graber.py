import datetime
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Graber:
    def __init__(self):
        self.url = "https://cdek.kz"
        self.ua = (
            "Mozilla/5.0 (X11; Linux x86_64)"
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        )

    def __init_options(self) -> Options:
        options = Options()
        options.headless = True

        return options

    def __init_headers(self) -> dict:
        headers = {"accept": "*/*", "user-agent": self.ua}
        return headers

    def grab_cookie(self) -> str:
        driver_options: Options = self.__init_options()
        cookie_str: str = ""

        with webdriver.Firefox(options=driver_options) as driver:
            driver.get("https://cdek.kz/track.html")
            cookies_list = driver.get_cookies()

            for cookie in cookies_list:
                if cookie["name"] == "_ym_isad":
                    cookie["value"] = 2

                if cookie["name"] == "tmr_reqNum":
                    cookie["value"] = 118

                if cookie["name"] == "sms":
                    cookie["value"] = "la2ojbl72emp6sfukavq44nbpd"

                cookie_str += f"{cookie['name']}={cookie['value']}; "
            cookie_str += "ILangCode=ru; HideCookieNotifyBox=Yes"

        return cookie_str


class Record:
    @staticmethod
    def store_cookie(filename: str = "cookies.txt") -> str:
        cookies: str = Graber().grab_cookie()
        with open(filename, "a+") as file:
            print(
                json.dumps(
                    {"cookie": cookies, "timestamp": str(datetime.datetime.now()),}
                ),
                file=file,
            )
        return cookies
