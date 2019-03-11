from json2table import convert
from st2common.runners.base_action import Action

from napalm import get_network_driver

__all__ = [
    'NapalmBaseAction'
]


class NapalmBaseAction(Action):
    """Base class for all NAPALM ST2 actions
    """

    def __init__(self, config):
        super(NapalmBaseAction, self).__init__(config)

    def get_driver(self, **std_kwargs):
        """Centralizes some of the setup logic for each action

        This will allow each action to more or less focus solely on the logic specific
        to its task
        """

        # Hostname is required
        hostname = std_kwargs['hostname']

        # These are not required, so we can default to None
        credentials = std_kwargs.get('credentials')
        driver = std_kwargs.get('driver')
        port = std_kwargs.get('port')
        htmlout = std_kwargs.get('htmlout', False)

        # Look up the driver  and if it's not given from the configuration file
        # Also overides the hostname since we might have a partial host i.e. from
        # syslog such as host1 instead of host1.example.com
        found_device = self.find_device_from_config(hostname, driver, credentials, port)

        login = self.get_credentials(found_device['credentials'])

        optional_args = {}

        if not found_device['port']:
            pass
        else:
            optional_args = {'port': int(found_device['port'])}

        if 'secret' in login:
            optional_args = {'secret': login['secret']}

        if 'key_file' in login:
            optional_args = {'key_file': str(login['key_file'])}
            login['password'] = None

        # Some actions like to use these params in log messages, or commands, etc.
        # So we tie to instance for easy lookup
        self.hostname = found_device['hostname']
        self.driver = found_device['driver']
        self.htmlout = htmlout

        return get_network_driver(self.driver)(
            hostname=str(found_device['hostname']),
            username=login['username'],
            password=login['password'],
            optional_args=optional_args
        )

    def get_credentials(self, credentials):
        """Looks up credentials section references in the device configuration
        """

        authconfig = self.config['credentials'].get(credentials, None)

        if not authconfig:
            raise ValueError('Can not find credentials group {}.'.format(credentials))

        if 'password' not in authconfig and 'key_file' not in authconfig:
            raise ValueError("Missing password or SSH key in credentials.")

        if authconfig['username'] is None:
            raise ValueError("Missing username in credentials.")

        return authconfig

    def find_device_from_config(self, search, driver=None, credentials=None, port=None):
        """Locates device in configuration based on search parameters
        """

        try:
            devices = self.config['devices']
        except KeyError:
            # Probably means the user needs to provide a config and/or
            # reload with `st2ctl reload --register-configs`, so we can
            # provide helpful error message
            message = ("Configuration Error: Please provide a pack config and ensure it's loaded "
                       " with `st2ctl reload --register-configs`")
            raise Exception(message)

        search = search.lower()

        # Set host_result here in case it's not found.
        host_result = search

        for d in devices:
            hostname = d['hostname'].lower()

            # Find the first device in the configuration which matches the
            # start of the hostname. Network devices don't often report
            # the FQDN in the syslog events for example.

            if hostname.startswith(search):
                # Driver has not been set by a parameter so set from config.
                if not driver:
                    driver = d['driver']

                # Credentials has not been set by a parameter so set from config.
                if not credentials:
                    credentials = d['credentials']

                # Port has not been set by a parameter so set from config.
                if not port:

                    # NOTE that this can also be None, and if it is, optional_args
                    # will be empty (meaning the NAPALM driver will impose its default)
                    port = d.get('port')

                # Set FQDN or hostname from the config, found in the match.
                host_result = hostname

                # Found first entry, no need to carry on.
                break

        # If we get here both credentials and driver should be set either from
        # the config file or passed as parameters. If the host is not found
        # in the config file then we can't get driver or credentials from the
        # config so they must be be passed as parameters manually, if not then
        # we fail.

        if not driver:
            raise ValueError('Can not find driver for host {}, try with '
                             'driver parameter.'.format(host_result))

        if not credentials:
            raise ValueError(('Can not find credential group for host {}, try with credentials '
                              'parameter.').format(host_result))

        if driver not in ["ios", "iosxr", "junos", "eos", "fortios", "ibm", "nxos",
                          "pluribus", "panos", "ros", "vyos", "nxos_ssh"]:
            raise ValueError('Driver "{}" is not a valid NAPALM Driver.'.format(driver))

        # Return, this will be the original search and parameters
        # if we didn't find anything
        return {
            "hostname": host_result,
            "port": port,
            "driver": driver,
            "credentials": credentials,
        }

    def html_out(self, to_convert):

        table_attributes = {"class": self.config['html_table_class']}

        return convert(to_convert, table_attributes=table_attributes)
