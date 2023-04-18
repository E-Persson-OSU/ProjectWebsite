from bs4 import BeautifulSoup
import requests
import re
import copy
from static.govdeals_cats import (
    GOVDEALS_LINK_CAT,
    GOVDEALS_CODES,
    GOVDEALS_LINK_CAT_MAX_ROWS,
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
        response = requests.get(url)
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
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {e}")
        return None


def get_rows(cc, mr):
    url = get_link(cat_code=cc, max_rows=mr)
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise an error if the response status code is not 200
        soup = BeautifulSoup(response.content, "html.parser")
        allrow = soup.find_all("div", id="boxx_row")
        rows = []
        for row in allrow:
            rows.append(row)
        return rows
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {e}")
        return None


def get_link(cat_code, max_rows=0):
    if max_rows > 0:
        return GOVDEALS_LINK_CAT_MAX_ROWS.format(cat_code, max_rows)
    else:
        return GOVDEALS_LINK_CAT.format(cat_code)


# takes a list of unparsed rows, returns the required contents as a list of dicts
def take_rows_give_contents(rows):
    contents = []
    for row in rows:
        content_dict = {
            "description": None,
            "location": None,
            "auction_close": None,
            "current_bid": None,
            "more_info_link": None,
            "photo_link": None,
        }
        soup = BeautifulSoup(row, "html.parser")
        content_dict["description"] = soup.find(id="result_col_2").find("a").text
        content_dict["location"] = soup.find(id="result_col_3").text
        content_dict["auction_close"] = (
            soup.find(id="result_col_4").find("label").text
            + soup.find(id="result_col_4").find("label").find("span").text
        )
        content_dict["current_bid"] = soup.find(id="bid_price").text
        content_dict["more_info_link"] = (
            soup.find(id="result_col_1").find("div").find("a")["href"]
        )
        content_dict["photo_link"] = soup.find(id="result_col_1").find("a")["href"]
        contents.append(copy.deepcopy(content_dict))
    return contents


"""
Web methods for querying database and populating webpage

"""

# pull entries from database when web page is loaded
# return them as a list of dictionaries
