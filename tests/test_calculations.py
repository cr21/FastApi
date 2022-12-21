from app.calculations import add


def test_add():
    res = add(1,2)
    assert res==3


test_add()