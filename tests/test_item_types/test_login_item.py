from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fixtures.valid_data import ValidData

    from ..fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

from pyonepassword.api.object_types import OPLoginItem

VALID_LOGIN_1 = "example-login-1"
VALID_LOGIN_2 = "example-login-2"


def test_login_item_010(valid_data: ValidData, expected_login_item_data: ExpectedLoginItemData):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.username == expected.username


def test_login_item_020(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.password == expected.password


def test_login_item_030(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.primary_url.href == expected.primary_url.href


def test_login_item_040(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.primary_url.label == expected.primary_url.label


def test_login_item_041(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    url_list = result.urls
    url = url_list[0]
    assert url.primary
    assert url.href == expected.primary_url.href
    assert url.label == expected.primary_url.label


def test_login_item_050(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected = expected_login_item_data.data_for_login(item_name)
    result = OPLoginItem(item_dict)

    assert result.primary_url.label == expected.primary_url.label


def test_login_item_060(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)
    result = OPLoginItem(item_dict)

    # "favorite" is true for Example Login 1
    assert result.favorite == expected.favorite


def test_login_item_070(valid_data: ValidData, expected_login_item_data):
    item_name = "Example Login 1"
    item_dict = valid_data.data_for_name(VALID_LOGIN_1)
    expected: ExpectedLogin = expected_login_item_data.data_for_login(
        item_name)
    result = OPLoginItem(item_dict)

    assert result.version == expected.version


# Example Login 2 has no URLs and favorite is not set
def test_login_item_080(valid_data: ValidData):
    item_dict = valid_data.data_for_name(VALID_LOGIN_2)
    result = OPLoginItem(item_dict)

    assert result.urls == []


def test_login_item_090(valid_data: ValidData):
    item_dict = valid_data.data_for_name(VALID_LOGIN_2)
    result = OPLoginItem(item_dict)

    assert result.primary_url is None


def test_login_item_100(valid_data: ValidData):
    item_dict = valid_data.data_for_name(VALID_LOGIN_2)
    result = OPLoginItem(item_dict)

    # "favorite" is unset for Example Login 2
    assert result.favorite is False
