from bs4 import BeautifulSoup
import requests
import re
import copy
from pathlib import Path
import json
import datetime
from dateutil import parser
from typing import List
from static.proxies import random_proxy
from services.base_logger import logger
from static.govdeals_cats import (
    GOVDEALS_LINK_CAT,
    GOVDEALS_CODES,
    GOVDEALS_LINK_CAT_MAX_ROWS,
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
}


def remove_escape_characters(text):
    # Define regex pattern to match escape characters
    escape_pattern = r"\\[nrt\xa0]"

    # Replace escape characters with their corresponding characters
    return re.sub(
        escape_pattern,
        lambda match: {
            "\\n": "\n",
            "\\r": "\r",
            "\\t": "\t",
            "\\xa0": " ",
        }[match.group()],
        text,
    )


"""
Worker methods for updating database


"""
# scrape website daily or when update button is pressed
# put entries in database


#
def get_max_rows(cat_code):
    url = get_link(cat_code)
    try:
        prox = random_proxy()
        logger.info("Using {} as proxy".format(prox["http"]))
        response = requests.get(url=url, headers=headers, proxies=prox)
        response.raise_for_status()  # raise an error if the response status code is not 200
        soup = BeautifulSoup(response.content, "html.parser")
        allstrong = soup.find_all("strong")
        line = ""
        max_rows = 0
        for tag in allstrong:
            if "through" in tag.text:
                line = tag.text
        pattern = r"\d+$"
        match = re.search(pattern, line)
        if match:
            number = int(match.group())
            max_rows = number
        else:
            print("No match found")
        return max_rows
    except (
        requests.exceptions.RequestException,
        ValueError,
        requests.exceptions.ConnectionError,
    ) as e:
        print(f"Error: {e}")
        return None


def get_rows(cc, mr) -> list:
    url = get_link(cat_code=cc, max_rows=mr)
    try:
        prox = random_proxy()
        logger.info("Using {} as a proxy".format(prox["http"]))
        response = requests.get(url=url, headers=headers, proxies=prox)
        response.raise_for_status()  # raise an error if the response status code is not 200
        soup = BeautifulSoup(response.content, "html.parser")
        allrow = soup.find_all("div", id="boxx_row")
        rows = []
        for row in allrow:
            rows.append(row)
        return rows
    except (
        requests.exceptions.RequestException,
        ValueError,
        requests.exceptions.ConnectionError,
    ) as e:
        print(f"Error: {e}")
        return None


def get_link(cat_code, max_rows=0) -> str:
    if max_rows > 0:
        return GOVDEALS_LINK_CAT_MAX_ROWS.format(cat_code, max_rows)
    else:
        return GOVDEALS_LINK_CAT.format(cat_code)


# takes a list of unparsed rows, returns the required contents as a list of dicts
def take_rows_give_contents(rows, gdlistings, cc):
    for row in rows:
        content_dict = {
            "description": None,
            "location": None,
            "auction_close": None,
            "current_bid": None,
            "info_link": None,
            "photo_link": None,
        }
        row = str(row)
        soup = BeautifulSoup(row, "html.parser")
        # Find the relevant elements in the HTML
        result_col_2 = soup.find(id="result_col_2")
        result_col_3 = soup.find(id="result_col_3")
        result_col_4 = soup.find(id="result_col_4")
        bid_price = soup.find(id="bid_price")
        result_col_1_div_a = soup.find(id="result_col_1").find("div").find("a")
        result_col_1_a = soup.find(id="result_col_1").find("a")

        # Extract the desired information from the elements
        content_dict["description"] = (
            result_col_2.find("a").text.strip() if result_col_2 else ""
        )
        content_dict["location"] = result_col_3.text.strip() if result_col_3 else ""
        auction_close_label = (
            result_col_4.find("label").text.strip() if result_col_4 else ""
        )
        auction_close_span = (
            result_col_4.find("label").find("span").text.strip() if result_col_4 else ""
        )
        content_dict["auction_close"] = (
            auction_close_label.strip() + auction_close_span.strip()
        )
        content_dict["current_bid"] = bid_price.text.strip() if bid_price else ""
        content_dict["info_link"] = (
            result_col_1_div_a["href"].strip() if result_col_1_div_a else ""
        )
        content_dict["photo_link"] = (
            result_col_1_a["href"].strip() if result_col_1_a else ""
        )

        # Add the information to the list of results
        for key, value in content_dict.items():
            content_dict[key] = (
                value.replace("\r", "")
                .replace("\n", "")
                .replace("\t", "")
                .replace("\xa0", "")
                .replace("Location:", "")
                .strip()
            )
        # change auction close time to integer for storage
        content_dict["auction_close"] = convert_datetime(content_dict["auction_close"])

        gdlistings.add_listing(copy.deepcopy(content_dict), cc)

    return gdlistings


# returns a GovDeals object containing a list of GovDealsListings
def gather_listings():
    cat_code_dict = copy.deepcopy(GOVDEALS_CODES)
    # Get max rows for all categories in a single HTTP request
    cat_max_rows = {k: get_max_rows(v) for k, v in cat_code_dict.items()}

    obj = GovDeals()
    for key, cat_code in cat_code_dict.items():
        rows = get_rows(cat_code, cat_max_rows[key])
        if rows is not None:
            take_rows_give_contents(rows, obj, cat_code)
    return obj


def load_json_dump():
    data_folder = Path("services/json-cache/")
    file_path = data_folder / "test_rows.json"
    with open(file_path, "r") as f:
        data = json.load(fp=f)
    return data


def convert_datetime(dt: str) -> int:
    knowntime = parser.parse(remove_duplicate_time(dt))
    return int(knowntime.timestamp())


def remove_duplicate_time(s: str) -> str:
    pattern = r"(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} [AP]M [A-Z]{2})(\d{1,2}:\d{2} [AP]M [A-Z]{2})$"
    match = re.search(pattern, s)
    if match:
        return s[: match.start(2)].strip()
    else:
        return s


class GovDealsListing:
    def __init__(self, gddict: dict, category: int):
        self._gddict = gddict
        self.category = category

    @property
    def itemid(self) -> str:
        return self._extract_id("itemid")

    @property
    def acctid(self) -> str:
        return self._extract_id("acctid")

    @property
    def listingid(self) -> str:
        return f"{self.acctid}{self.itemid}"

    @property
    def description(self) -> str:
        return self._gddict.get("description", "")

    @property
    def location(self) -> str:
        return self._gddict.get("location", "")

    @property
    def auction_close(self) -> str:
        # stored as integer, converted back to string for use
        dt = datetime.datetime.fromtimestamp(int(self._gddict.get("auction_close", "")))
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def current_bid(self) -> str:
        return self._gddict.get("current_bid", "")

    @property
    def info_link(self) -> str:
        return self._gddict.get("info_link", "")

    @property
    def photo_link(self) -> str:
        return self._gddict.get("photo_link", "")

    def _extract_id(self, key: str) -> str:
        id_str = self._gddict.get("info_link", "")
        id_dict = dict(x.split("=") for x in id_str.split("&") if "=" in x)
        return id_dict.get(key, "")

    def __repr__(self) -> str:
        return f"GovDealsListing({self.listingid})"


class GovDeals:
    def __init__(self):
        self.listings: List[GovDealsListing] = []

    def add_listing(self, gddict: dict, category: int) -> None:
        self.listings.append(GovDealsListing(gddict, category))

    def all_listings(self) -> List[GovDealsListing]:
        return self.listings

    def __iter__(self):
        return iter(self.listings)


"""
Web methods for querying database and populating webpage

"""

# pull entries from database when web page is loaded
# return them as a list of dictionaries
