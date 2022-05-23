import os
import tempfile
from pathlib import Path

from .valid_data import ValidData

VALID_OP_CONFIG_KEY = "example-op-config"
VALID_OP_CONFIG_NO_SHORTHAND_KEY = "example-op-config-no-latest-shorthand"


class ValidOPCLIConfig:
    def __init__(self, location_env_var='HOME', config_text=None, valid_data_key=VALID_OP_CONFIG_KEY):
        self._new_home = None
        self._old_home = None
        self._tempdir = tempfile.TemporaryDirectory()

        # reset $HOME to something useless
        # of location_env_var is HOME, we'll reset it later
        new_home = "/dev/null"
        self._old_home = os.environ['HOME']
        self._old_xdg = os.environ.get("XDG_CONFIG_HOME")
        os.environ['HOME'] = new_home

        if location_env_var is not None:
            os.environ[location_env_var] = self._tempdir.name
        # save whatever we set HOME to for later comparison & restore
        self._new_home = os.environ['HOME']
        self._new_xdg = os.environ.get('XDG_CONFIG_HOME')

        if location_env_var != "XDG_CONFIG_HOME":
            # if we didn't explicitly need XDG_CONFIG_HOME, make sure it hasn't been set
            os.environ.pop('XDG_CONFIG_HOME', None)

        op_config_path = Path(self._tempdir.name, ".config", "op")
        op_config_path.mkdir(parents=True)
        op_config_path = Path(op_config_path, "config")
        if config_text is None:
            config_text = ValidData().data_for_name(valid_data_key)
        with open(op_config_path, "w") as config:
            config.write(config_text)
        self._op_config_path = op_config_path

    def __del__(self):
        if os.environ.get('HOME') == self._new_home:
            os.environ['HOME'] = self._old_home

        if os.environ.get('XDG_CONFIG_HOME') == self._new_xdg:
            if self._old_xdg is not None:
                os.environ['XDG_CONFIG_HOME'] = self._old_xdg
            else:
                # we can't set an env variable to None. You have to delete it
                os.environ.pop('XDG_CONFIG_HOME', None)
