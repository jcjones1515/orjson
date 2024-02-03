import decimal

import pytest
import orjson


class C:
    c: "C"

    def __del__(self):
        orjson.loads('"' + "a" * 10000 + '"')


def test_reentrant():
    c = C()
    c.c = c
    del c

    orjson.loads("[" + "[]," * 1000 + "[]]")


def test_reentrant_via_exception():
    def another_encoder(o):
        # do something but ultimately
        raise TypeError("bad")

    def default_f(o):
        try:
            if type(o) == set:
                return list(o)
            else:
                another_encoder(o)
        except TypeError as t:
            print(f"Caught TypeError for {o}")
            raise t

    with pytest.raises(orjson.JSONEncodeError):
        orjson.dumps([[{decimal.Decimal("0.0842389659712649442845")}] * 1000], default=default_f)
