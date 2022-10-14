from __future__ import annotations

from typing import TYPE_CHECKING

from pyonepassword.api.object_types import (
    OPLoginItemNewPrimaryURL,
    OPLoginItemNewURL,
    OPNewLoginItem
)
from pyonepassword.op_items._new_fields import OPNewStringField
from pyonepassword.op_items.item_section import OPItemField, OPSection

if TYPE_CHECKING:
    from ..fixtures.valid_data import ValidData


def test_new_login_item_url_01():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewURL(url, label)
    assert new_url.href == url


def test_new_login_item_url_02():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewURL(url, label)
    assert new_url.label == label


def test_new_login_item_url_03():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewURL(url, label)
    assert not new_url.primary


def test_new_login_item_url_04():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewURL(url, label, primary=True)
    assert new_url.primary


def test_new_login_item_url_05():
    url = "https://example.com/index.html"
    label = "Example URL"

    new_url = OPLoginItemNewPrimaryURL(url, label)
    assert new_url.primary


def test_new_login_item_01():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    url_label = "Example URL"

    new_url = OPLoginItemNewPrimaryURL(primary_url, url_label)
    new_login = OPNewLoginItem(title, username,  url=new_url)
    assert new_login.username == username


def test_new_login_item_02():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    url_label = "Example URL"

    new_url = OPLoginItemNewPrimaryURL(primary_url, url_label)
    new_login = OPNewLoginItem(title, username,  url=new_url)
    assert new_login.primary_url.href == new_url.href


def test_new_login_item_03():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    primary_url_label = "Example URL"

    second_url = "https://second-example.com"
    second_url_label = "Secondary URL"

    primary_url = OPLoginItemNewPrimaryURL(primary_url, primary_url_label)
    second_url = OPLoginItemNewURL(second_url, second_url_label)

    new_login = OPNewLoginItem(title, username,  url=primary_url)

    new_login.add_url(second_url)
    assert new_login.urls[1].href == second_url.href


def test_new_login_item_04():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    primary_url_label = "Example URL"

    second_url = "https://second-example.com"
    second_url_label = "Secondary URL"

    primary_url = OPLoginItemNewPrimaryURL(primary_url, primary_url_label)
    second_url = OPLoginItemNewURL(second_url, second_url_label)

    new_login = OPNewLoginItem(title, username,  url=primary_url)

    new_login.add_url(second_url)
    assert new_login.primary_url.href == primary_url.href


def test_new_login_item_05():
    username = "test_username"
    title = "Test Login Item"
    primary_url = "https://example.com/index.html"
    primary_url_label = "Example URL"
    primary_url = OPLoginItemNewPrimaryURL(primary_url, primary_url_label)

    new_login = OPNewLoginItem(title, username)

    new_login.add_url(primary_url)
    assert new_login.primary_url.href == primary_url.href


def test_new_login_item_06(valid_data: ValidData):
    """
    Create:
        - two new fields
        - A section associated with the fields
        - An OPNewLoginItem object with the fields and the section
    Verify:
        - field_1 is property added to the login item
    """
    section_dict = valid_data.data_for_name("example-item-section-1")
    field_dict_1 = valid_data.data_for_name("example-field-no-uuid-1")
    field_dict_2 = valid_data.data_for_name("example-field-no-uuid-2")
    existing_section = OPSection(section_dict)

    existing_field = OPItemField(field_dict_1)
    new_field_1 = OPNewStringField.from_field(
        existing_field, section=existing_section)
    existing_field = OPItemField(field_dict_2)
    new_field_2 = OPNewStringField.from_field(
        existing_field, section=existing_section)
    fields = [new_field_1, new_field_2]
    sections = [existing_section]

    username = "test_username"
    title = "Test Login Item"

    new_login = OPNewLoginItem(
        title, username, fields=fields, sections=sections)

    result = new_login.field_by_id(new_field_1.field_id)
    assert result.value == new_field_1.value


def test_new_login_item_07(valid_data: ValidData):
    """
    Create:
        - A section associated with existing (as opposed to new) fields
        - An OPNewLoginItem object with the fields and the section
    Verify:
        - field_1 is properly added
    """
    section_dict = valid_data.data_for_name("example-item-section-1")
    field_dict_1 = valid_data.data_for_name("example-field-no-uuid-1")
    field_dict_2 = valid_data.data_for_name("example-field-no-uuid-2")
    existing_section = OPSection(section_dict)

    existing_field_1 = OPItemField(field_dict_1)
    existing_field_1["section"] = existing_section
    existing_section.register_field(existing_field_1)

    existing_field_2 = OPItemField(field_dict_2)
    existing_field_2["section"] = existing_section
    existing_section.register_field(existing_field_2)

    fields = [existing_field_1, existing_field_2]
    sections = [existing_section]

    username = "test_username"
    title = "Test Login Item"

    new_login = OPNewLoginItem(
        title, username, fields=fields, sections=sections)

    result = new_login.field_by_id(existing_field_1.field_id)
    assert result.value == existing_field_1.value


def test_new_login_item_08(valid_data: ValidData):
    """
    Create:
        - two new fields with UUID IDs
        - A section associated with the fields
        - An OPNewLoginItem object with the fields and the section
    Verify:
        - fields' IDs don't get regenerated after creating the login item
    """
    section_dict = valid_data.data_for_name("example-item-section-1")
    field_dict_1 = valid_data.data_for_name("example-field-with-uuid-1")
    field_dict_2 = valid_data.data_for_name("example-field-with-uuid-2")
    existing_section = OPSection(section_dict)

    existing_field = OPItemField(field_dict_1)
    new_field_1 = OPNewStringField.from_field(
        existing_field, section=existing_section)
    existing_field = OPItemField(field_dict_2)
    new_field_2 = OPNewStringField.from_field(
        existing_field, section=existing_section)
    fields = [new_field_1, new_field_2]
    sections = [existing_section]

    username = "test_username"
    title = "Test Login Item"

    new_login = OPNewLoginItem(
        title, username, fields=fields, sections=sections)

    result_1 = new_login.field_by_id(new_field_1.field_id)
    result_2 = new_login.field_by_id(new_field_2.field_id)

    # we wouldn't have gotten this far if field_id was regenerated
    # but may as well assert equality while we're here
    # new fields IDs shouldn't have gotten regenerated even though
    # they're UUIDs, since the fields are OPNewItemField instances
    assert result_1.field_id == new_field_1.field_id
    assert result_2.field_id == new_field_2.field_id
