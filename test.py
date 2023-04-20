from services import govdeals as gd


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


if __name__ == "__main__":
    for_db = gd.gather_listings()
    print(for_db[0][0])
