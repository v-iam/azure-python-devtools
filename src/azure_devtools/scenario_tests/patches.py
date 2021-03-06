# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .exceptions import AzureTestError
from .const import MOCKED_SUBSCRIPTION_ID, MOCKED_TENANT_ID


def patch_time_sleep_api(unit_test):
    def _time_sleep_skip(*_):
        return

    _mock_in_unit_test(unit_test, 'time.sleep', _time_sleep_skip)


def patch_long_run_operation_delay(unit_test):
    def _shortcut_long_run_operation(*args, **kwargs):  # pylint: disable=unused-argument
        return

    _mock_in_unit_test(unit_test,
                       'msrestazure.azure_operation.AzureOperationPoller._delay',
                       _shortcut_long_run_operation)


def _mock_in_unit_test(unit_test, target, replacement):
    import mock
    import unittest

    if not isinstance(unit_test, unittest.TestCase):
        raise AzureTestError('Patches can be only called from a unit test')

    mp = mock.patch(target, replacement)
    mp.__enter__()
    unit_test.addCleanup(mp.__exit__)
