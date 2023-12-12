from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyonepassword import OP


import pytest

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_user_edit_travel_mode")
def test_user_edit_010(signed_in_team_account_op: OP):
    """
    Test: OP.user_edit()
        - set travel mode on for a user
        - set travel mode off for the same user
    Verify:
        - No exception is raised for either operation
        - The user name is correctly converted to the expected user ID for both edit operations

    """
    # There isn't, as of this writing, any way to verify travel mode has been turned
    # on or off
    # nothing about travel mode shows up in `op user get`,
    # and for reasons that aren't clear, travel mode restrictions only affect the apps,
    # not `op item get/list` or `op vault list`, so it's not possible to check if a user
    # has/does not have access to something when travel mode is enabled
    #
    # so there isn't really much to test here other than:
    # - we're constructing the CLI arguments correctly
    # - mock-op has a corresponding response to those CLI args
    # - nothing blew up when the response generator ran `op` with those args
    user_id = "Example User"
    signed_in_team_account_op.user_edit(user_id, travel_mode=True)
    signed_in_team_account_op.user_edit(user_id, travel_mode=False)
