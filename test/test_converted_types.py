# -*- coding: UTF-8 -*-
"""test_converted_types.py - tests for decoding data to their logical data types."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
from decimal import Decimal
import pandas as pd

from parquet import parquet_thrift as pt
from parquet.converted_types import convert


def test_int32():
    """Test decimal data stored as int32."""
    schema = pt.SchemaElement(
        type=pt.Type.INT32,
        name="test",
        converted_type=pt.ConvertedType.DECIMAL,
        scale=10,
        precision=9
    )

    assert (convert(pd.Series([9876543210]), schema)[0] - 9.87654321) < 0.01


def test_date():
    """Test int32 encoding a date."""
    schema = pt.SchemaElement(
        type=pt.Type.INT32,
        name="test",
        converted_type=pt.ConvertedType.DATE,
    )
    assert (convert(pd.Series([731888]), schema)[0] ==
            pd.to_datetime([datetime.date(2004, 11, 3)]))


def test_time_millis():
    """Test int32 encoding a timedelta in millis."""
    schema = pt.SchemaElement(
        type=pt.Type.INT32,
        name="test",
        converted_type=pt.ConvertedType.TIME_MILLIS,
    )
    assert convert(pd.Series([731888]), schema)[0] == datetime.timedelta(milliseconds=731888)


def test_timestamp_millis():
    """Test int64 encoding a datetime."""
    schema = pt.SchemaElement(
        type=pt.Type.INT64,
        name="test",
        converted_type=pt.ConvertedType.TIMESTAMP_MILLIS,
    )
    assert convert(pd.Series([1099511625014]), schema)[0] == datetime.datetime(2004, 11, 3, 19, 53, 45, 14 * 1000)


def test_utf8():
    """Test bytes representing utf-8 string."""
    schema = pt.SchemaElement(
        type=pt.Type.BYTE_ARRAY,
        name="test",
        converted_type=pt.ConvertedType.UTF8
    )
    data = b'\xc3\x96rd\xc3\xb6g'
    assert convert(pd.Series([data]), schema)[0] == "Ördög"


def test_json():
    """Test bytes representing json."""
    schema = pt.SchemaElement(
        type=pt.Type.BYTE_ARRAY,
        name="test",
        converted_type=pt.ConvertedType.JSON
    )
    assert convert(pd.Series([b'{"foo": ["bar", "\\ud83d\\udc7e"]}']),
                          schema)[0] == {'foo': ['bar', '👾']}


def test_bson():
    """Test bytes representing bson."""
    schema = pt.SchemaElement(
        type=pt.Type.BYTE_ARRAY,
        name="test",
        converted_type=pt.ConvertedType.BSON
    )
    assert convert(pd.Series(
            [b'&\x00\x00\x00\x04foo\x00\x1c\x00\x00\x00\x020'
             b'\x00\x04\x00\x00\x00bar\x00\x021\x00\x05\x00\x00\x00\xf0\x9f\x91\xbe\x00\x00\x00']),
            schema)[0] == {'foo': ['bar', '👾']}


def test_uint16():
    """Test decoding int32 as uint16."""
    schema = pt.SchemaElement(
        type=pt.Type.INT32,
        name="test",
        converted_type=pt.ConvertedType.UINT_16
    )
    assert convert(pd.Series([-3]), schema)[0] == 65533


def test_uint32():
    """Test decoding int32 as uint32."""
    schema = pt.SchemaElement(
        type=pt.Type.INT32,
        name="test",
        converted_type=pt.ConvertedType.UINT_32
    )
    assert convert(pd.Series([-6884376]), schema)[0] == 4288082920


def test_uint64():
    """Test decoding int64 as uint64."""
    schema = pt.SchemaElement(
        type=pt.Type.INT64,
        name="test",
        converted_type=pt.ConvertedType.UINT_64
    )
    assert convert(pd.Series([-6884376]), schema)[0] == 18446744073702667240