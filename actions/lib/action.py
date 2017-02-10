import socket
from json2table import convert
from st2actions.runners.pythonrunner import Action


__all__ = [
    'NapalmBaseAction'
]


class NapalmBaseAction(Action):
    """Base class for all NAPALM ST2 actions
    """

    def __init__(self, config):
        super(NapalmBaseAction, self).__init__(config)

    def get_credentials(self, credentials):

        authconfig = self.config['credentials'].get(credentials, None)

        if not authconfig:
            raise ValueError('Can not find credentials group {}.'.format(credentials))

        if authconfig['password'] is None:
            raise ValueError("Missing password in credentials.")

        if authconfig['username'] is None:
            raise ValueError("Missing username in credentials.")

        return authconfig

    def find_device_from_config(self, search, host_ip=None, driver=None, credentials=None):

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

        # If the IP address is given we don't need to work it out otherwise
        # resolve the hostname. Check for string None - thinking jinja sometimes
        # converts to a string.
        if not host_ip or host_ip == "None":
            host_ip = socket.gethostbyname(host_result)

        # Return, this will be the original search and parameters
        # if we didn't find anything
        #
        return (host_result, host_ip, driver, credentials)

    def html_out(self, to_convert):

        table_attributes = {"class": self.config['html_table_class']}

        return convert(to_convert, table_attributes=table_attributes)
