import numpy as np
import pytest

from prettyprinter import install_extras, pformat

install_extras(["numpy"])


@pytest.mark.parametrize('nptype', (
    np.sctypes["uint"] +
    np.sctypes["int"] +
    np.sctypes["float"]
))
def test_numpy_numeric_types(nptype):
    val = nptype(1)
    py_val = val.item()

    if type(py_val) in (int, float):
        inner_printed = pformat(py_val)
    else:
        # numpy renders types such as float128,
        # that are not representable in native Python
        # types, with Python syntax
        inner_printed = repr(py_val)

    expected = "numpy.{}({})".format(nptype.__name__, inner_printed)
    assert pformat(val) == expected


def test_numpy_bool_type():
    assert pformat(np.bool_(False)) == "numpy.bool_(False)"
    assert pformat(np.bool_(True)) == "numpy.bool_(True)"


def test_array():
    assert pformat(np.array([0, 1])) == "numpy.ndarray([0, 1])"
    assert pformat(np.array([0., 1.])) == "numpy.ndarray([0.0, 1.0])"
    assert pformat(np.array([0, 1], dtype=np.uint8)) == "numpy.ndarray([0, 1], dtype='uint8')"
    assert pformat(np.array(["a", "b"])) == "numpy.ndarray(['a', 'b'], dtype='<U1')"
    assert pformat(np.array([("a", 1)], [("field1", str), ("field2", int)])) \
        == "numpy.ndarray([('', 1)], dtype=[('field1', '<U'), ('field2', '<i8')])"


def test_masked_array():
    # Check that masked arrays don't go through the normal array pprinter
    # (they require their own algoithm, which is not implemented yet).
    array = np.ma.array([0, 1])
    assert pformat(array) == repr(array)
