from services import govdeals as gd
import json

def test_max_rows():
    max_rows = gd.get_max_rows(28)
    print(max_rows)
    return max_rows


def test_get_rows(mr):
    rows = gd.get_rows(28, mr)
    print(len(rows))
    return rows


def test_trgc(rows):
    contents = gd.take_rows_give_contents(rows)
    print(len(contents))
    print(contents[0])

def create_json_dump(dump):
    with open('static\\bin\\test_rows.json', 'w') as f:
        json.dump(dump,fp=f)
    print('Flush!')

if __name__ == "__main__":
    for_db = gd.gather_listings()
    create_json_dump(for_db)
