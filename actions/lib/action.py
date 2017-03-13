from json2table import convert
from st2actions.runners.pythonrunner import Action

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
        found_device = self.find_device_from_config(hostname, driver, credentials)

        login = self.get_credentials(found_device['credentials'])

        if not port:
            optional_args = None
        else:
            optional_args = {'port': str(port)}

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

        if authconfig['password'] is None:
            raise ValueError("Missing password in credentials.")

        if authconfig['username'] is None:
            raise ValueError("Missing username in credentials.")

        return authconfig

    def find_device_from_config(self, search, driver=None, credentials=None):
        """Locates device in configuration based on search parameters
        """

        devices = self.config['devices']

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
            raise ValueError('Can not find driver for host {}, try with \
                            driver parameter.'.format(host_result))

        if not credentials:
            raise ValueError(('Can not find credential group for host {}, try with credentials'
                              'parameter.').format(host_result))

        if driver not in ["ios", "iosxr", "junos", "eos", "fortios", "ibm", "nxos",
                          "pluribus", "panos", "ros", "vyos"]:
            raise ValueError('Driver "{}" is not a valid NAPALM Driver.'.format(driver))

        # Return, this will be the original search and parameters
        # if we didn't find anything
        return {
            "hostname": host_result,
            "driver": driver,
            "credentials": credentials,
        }

    def html_out(self, to_convert):

        table_attributes = {"class": self.config['html_table_class']}

        return convert(to_convert, table_attributes=table_attributes)
