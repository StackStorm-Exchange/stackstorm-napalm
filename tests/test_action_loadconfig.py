import mock
import yaml

from st2tests.base import BaseActionTestCase
from loadconfig import NapalmLoadConfig

from napalm.base import exceptions


class NapalmLoadConfigTestCase(BaseActionTestCase):
    __test__ = True
    action_cls = NapalmLoadConfig

    def setUp(self):
        super(NapalmLoadConfigTestCase, self).setUp()

        self.full_config = yaml.safe_load(self.get_fixture_content('full.yaml'))
        self.default_kwargs = {
            'hostname': 'localhost',
            'driver': 'junos',
            'config_file': None,
            'config_text': '/usr/local/etc/junos_config',
            'method': 'merge',
            'inline_transfer': False,
            'credentials': 'core',
        }

    def test_run_without_hostname_parameter(self):
        del self.default_kwargs['hostname']

        action = self.get_action_instance(self.full_config)

        with self.assertRaises(KeyError):
            action.run(**self.default_kwargs)

    def test_run_with_invalid_driver_parameter(self):
        self.default_kwargs['driver'] = 'invalid_driver'

        action = self.get_action_instance(self.full_config)
        result = action.run(**self.default_kwargs)

        self.assertFalse(result[0])
        self.assertEqual(result[1], 'Driver "invalid_driver" is not a valid NAPALM Driver.')

    def test_run_without_credentials(self):
        del self.default_kwargs['credentials']

        action = self.get_action_instance(self.full_config)
        result = action.run(**self.default_kwargs)

        self.assertFalse(result[0])
        self.assertEqual(result[1].find('Can not find credential group for host localhost'), 0)

    @mock.patch('lib.action.get_network_driver')
    def test_run_with_incorrect_config_parameter_using_replace_method(self, mock_method):
        # set parameter to fail
        self.default_kwargs['config_text'] = 'invalid command'
        self.default_kwargs['method'] = 'replace'

        # prepare mock processing
        err_msg = 'syntax error'
        mock_device = mock.MagicMock()
        mock_device.load_replace_candidate.side_effect = exceptions.ReplaceConfigException(err_msg)
        mock_device.__enter__.return_value = mock_device

        mock_driver = mock.MagicMock()
        mock_driver.return_value = mock_device
        mock_method.return_value = mock_driver

        action = self.get_action_instance(self.full_config)
        result = action.run(**self.default_kwargs)

        self.assertFalse(result[0])
        self.assertEqual(result[1], err_msg)

    @mock.patch('lib.action.get_network_driver')
    def test_run_with_incorrect_config_parameter_using_merge_method(self, mock_method):
        # set parameter to fail
        self.default_kwargs['config_text'] = 'invalid command'
        self.default_kwargs['method'] = 'merge'

        # prepare mock processing
        err_msg = 'syntax error'
        mock_device = mock.MagicMock()
        mock_device.load_merge_candidate.side_effect = exceptions.MergeConfigException(err_msg)
        mock_device.__enter__.return_value = mock_device

        mock_driver = mock.MagicMock()
        mock_driver.return_value = mock_device
        mock_method.return_value = mock_driver

        action = self.get_action_instance(self.full_config)
        result = action.run(**self.default_kwargs)

        self.assertFalse(result[0])
        self.assertEqual(result[1], err_msg)

    @mock.patch('lib.action.get_network_driver')
    def test_run_with_correct_parameters(self, mock_method):
        action = self.get_action_instance(self.full_config)
        result = action.run(**self.default_kwargs)

        self.assertTrue(result[0])
        self.assertEqual(result[1].find('load (merge) successful'), 0)

    @mock.patch('lib.action.get_network_driver')
    def test_run_without_both_config_file_and_text(self, mock_method):
        self.default_kwargs['config_file'] = self.default_kwargs['config_text'] = None

        action = self.get_action_instance(self.full_config)
        result = action.run(**self.default_kwargs)

        self.assertFalse(result[0])
        self.assertEqual(result[1], 'Specify either config_file or config_text')
