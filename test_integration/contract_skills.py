#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=no-self-use
import pytest

from test_integration.integration_test_base import execute_cmd


class ContractSkills:
    def is_auto_mode(self):
        return True

    def get_skill_name(self):
        raise NotImplementedError('You should provide the commands to execute.')

    def get_commands_to_execute(self):
        raise NotImplementedError('You should provide the commands to execute.')

    def get_commands_expected(self):
        raise NotImplementedError('You should provide the commands expected.')

    @pytest.mark.dependency()
    def test_install(self, my_clai_module):
        if self.is_auto_mode():
            execute_cmd(my_clai_module, "clai auto")
        skill_name = self.get_skill_name()
        command_select = f"clai activate {skill_name}"

        command_executed = execute_cmd(my_clai_module, command_select)

        assert f"☑\x1b[32m {skill_name} (Installed)" in command_executed

    @pytest.mark.dependency(depends=['test_install'])
    def test_skill_values(self, my_clai_module, command, command_expected):
        command_executed = execute_cmd(my_clai_module, command)
        assert command_expected in command_executed
