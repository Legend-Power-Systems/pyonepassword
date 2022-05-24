from __future__ import annotations

from typing import TYPE_CHECKING, List

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from pyonepassword import OP

    from .fixtures.expected_vault_data import (
        ExpectedVaultListData,
        ExpectedVaultListEntry
    )

from pyonepassword import (
    OPInvalidVaultListException,
    OPVaultDescriptor,
    OPVaultDescriptorList
)

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def _sanity_check_vault_list(vault_list, expected_list):
    assert isinstance(vault_list, OPVaultDescriptorList)
    assert len(vault_list) > 0
    assert len(vault_list) == len(expected_list)


def test_vault_list_all_vaults_01(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    expected: List[ExpectedVaultListEntry]
    result: OPVaultDescriptorList
    expected = expected_vault_list_data.data_for_key("all-vaults")
    result = signed_in_op.vault_list()

    _sanity_check_vault_list(result, expected)

    result_ids = {vault_obj.unique_id for vault_obj in result}
    expected_ids = {entry.unique_id for entry in expected}
    assert result_ids == expected_ids


def test_vault_list_all_vaults_02(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    epected_vault_list: List[ExpectedVaultListEntry]
    expected: ExpectedVaultListEntry

    expected_vault_list = expected_vault_list_data.data_for_key("all-vaults")
    expected = expected_vault_list[0]
    result = signed_in_op.vault_list()

    _sanity_check_vault_list(result, expected_vault_list)

    vault_entry = result[0]

    assert isinstance(vault_entry, OPVaultDescriptor)
    assert vault_entry.unique_id == expected.unique_id


def test_vault_list_all_vaults_03(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    epected_vault_list: List[ExpectedVaultListEntry]
    expected: ExpectedVaultListEntry

    expected_vault_list = expected_vault_list_data.data_for_key("all-vaults")
    expected = expected_vault_list[2]
    result = signed_in_op.vault_list()

    _sanity_check_vault_list(result, expected_vault_list)

    vault_entry = result[2]

    assert isinstance(vault_entry, OPVaultDescriptor)
    assert vault_entry.name == expected.name


def test_vault_list_example_user_01(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    expected: List[ExpectedVaultListEntry]
    result: OPVaultDescriptorList

    expected = expected_vault_list_data.data_for_key("user-example-user")
    result = signed_in_op.vault_list(
        user_name_or_id="example_user@example.email")

    _sanity_check_vault_list(result, expected)

    result_ids = {vault_obj.unique_id for vault_obj in result}
    expected_ids = {entry.unique_id for entry in expected}
    assert result_ids == expected_ids


def test_vault_list_example_user_02(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    epected_vault_list: List[ExpectedVaultListEntry]
    expected: ExpectedVaultListEntry

    expected_vault_list = expected_vault_list_data.data_for_key(
        "user-example-user")
    expected = expected_vault_list[0]
    result = signed_in_op.vault_list(
        user_name_or_id="example_user@example.email")
    _sanity_check_vault_list(result, expected_vault_list)

    vault_entry = result[0]

    assert isinstance(vault_entry, OPVaultDescriptor)
    assert vault_entry.unique_id == expected.unique_id


def test_vault_list_example_user_03(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    epected_vault_list: List[ExpectedVaultListEntry]
    expected: ExpectedVaultListEntry

    expected_vault_list = expected_vault_list_data.data_for_key(
        "user-example-user")
    expected = expected_vault_list[2]
    result = signed_in_op.vault_list(
        user_name_or_id="example_user@example.email")

    _sanity_check_vault_list(result, expected_vault_list)

    vault_entry = result[2]

    assert isinstance(vault_entry, OPVaultDescriptor)
    assert vault_entry.name == expected.name


def test_vault_list_team_members_01(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    expected: List[ExpectedVaultListEntry]
    result: OPVaultDescriptorList

    expected = expected_vault_list_data.data_for_key("group-team-members")
    result = signed_in_op.vault_list(group_name_or_id="Team Members")

    _sanity_check_vault_list(result, expected)

    result_ids = {vault_obj.unique_id for vault_obj in result}
    expected_ids = {entry.unique_id for entry in expected}
    assert result_ids == expected_ids


def test_vault_list_team_members_02(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    epected_vault_list: List[ExpectedVaultListEntry]
    expected: ExpectedVaultListEntry

    expected_vault_list = expected_vault_list_data.data_for_key(
        "group-team-members")
    expected = expected_vault_list[0]
    result = signed_in_op.vault_list(group_name_or_id="Team Members")
    vault_entry = result[0]

    _sanity_check_vault_list(result, expected_vault_list)

    assert isinstance(vault_entry, OPVaultDescriptor)
    assert vault_entry.unique_id == expected.unique_id


def test_vault_list_team_members_03(signed_in_op: OP, expected_vault_list_data: ExpectedVaultListData):
    epected_vault_list: List[ExpectedVaultListEntry]
    expected: ExpectedVaultListEntry

    expected_vault_list = expected_vault_list_data.data_for_key(
        "group-team-members")
    expected = expected_vault_list[0]
    result = signed_in_op.vault_list(group_name_or_id="Team Members")
    vault_entry = result[0]

    _sanity_check_vault_list(result, expected_vault_list)

    assert isinstance(vault_entry, OPVaultDescriptor)
    assert vault_entry.name == expected.name


def test_vault_list_malformed_json_01(invalid_data):
    malformed_json = invalid_data.data_for_name("malformed-vault-list-json")

    with pytest.raises(OPInvalidVaultListException):
        OPVaultDescriptorList(malformed_json)
