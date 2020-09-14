import requests
from typing import Optional
import dataclasses


@dataclasses.dataclass
class HTTPSStatus:
    url: str
    error: Optional[str]

    @property
    def ok(self):
        return self.error is None


def check_https(url: str) -> HTTPSStatus:
    surl = url.replace("http:", "https:")
    try:
        res = requests.get(surl, timeout=2)
        return HTTPSStatus(surl, None) if res.ok else HTTPSStatus(url, str(res.reason))
    except requests.exceptions.SSLError:
        return HTTPSStatus(url, "SSLError")
    except requests.exceptions.ConnectTimeout:
        return HTTPSStatus(url, "ConnectTimeout")
    except Exception as e:
        return HTTPSStatus(url, str(e))


year = 2020
cours = 3
req_url = f"https://api.moemoe.tokyo/anime/v1/master/{year}/{cours}"

data = requests.get(req_url).json()
for anime in data:
    title = anime["title"]
    url = anime["public_url"]
    https = check_https(url)
    supports_https = "✅" if https.ok else "❌"
    reason = "" if https.ok else f"...<<{https.error}>>"
    print(f"{supports_https} {title}{reason} {url}")
