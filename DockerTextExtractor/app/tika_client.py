import requests
from tenacity import retry, stop_after_attempt, wait_fixed

TIKA_URL = "http://tika:9998/tika"

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def extract_text(file_path):

    headers = {
        "Accept": "text/plain"
    }

    with open(file_path, "rb") as f:
        r = requests.put(
            TIKA_URL,
            data=f,
            headers=headers,
            timeout=120
        )

    r.raise_for_status()
    return r.text