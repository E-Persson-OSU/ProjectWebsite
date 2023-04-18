from services import govdeals as gd


def test_max_rows():
    max_rows = gd.get_max_rows(28)
    print(max_rows)
    return max_rows


def test_get_rows(mr):
    rows = gd.get_rows(22, mr)
    print(len(rows))
    print(rows[0])
    return rows


def test_trgc(rows):
    contents = gd.take_rows_give_contents(rows)
    print(len(contents))
    for key in contents[0].keys:
        print("{}: {}".format(key, contents[0][key]))


if __name__ == "__main__":
    max_rows = test_max_rows()
    rows = test_get_rows(max_rows)
    test_trgc(rows)
