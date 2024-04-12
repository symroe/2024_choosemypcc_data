import json
import time
from pathlib import Path
from urllib.parse import urljoin

import requests

session = requests.Session()

DATA_PATH = Path("data")
DATA_PATH.mkdir(exist_ok=True)
BASE_URL = "https://choosemypcc.org.uk/wp-json/wp/v2/"


def save_person_json(person_json):
    person_path = DATA_PATH / "people" / f"{person_json['id']}.json"
    person_path.parent.mkdir(exist_ok=True, parents=True)
    with person_path.open("w") as f:
        f.write(json.dumps(person_json, indent=4))


def process_response(response_json):
    for candidate in response_json:
        save_person_json(candidate)


def iter_candidates():
    params = {
        "page": 1,
    }
    url = urljoin(BASE_URL, "candidate")
    while url:
        time.sleep(1)
        page_req = session.get(url, params=params)
        if page_req.status_code != 200:
            break
        data = page_req.json()
        process_response(data)
        params["page"] += 1


def main():
    iter_candidates()


if __name__ == "__main__":
    main()
