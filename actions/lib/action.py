from napalm import get_network_driver

from st2actions.runners.pythonrunner import Action

__all__ = [
    'NapalmBaseAction'
]

class NapalmBaseAction(Action):

    def __init__(self, config):
        super(NapalmBaseAction, self).__init__(config)

    def _get_credentials(self, credentials):

        authconfig = self.config['credentials'].get(credentials, None)

        if not authconfig:
            raise ValueError('Can not find credentials group {}.'.format(credentials))

        if authconfig['password'] is None:
            raise ValueError("Missing password in credentials.")

        if authconfig['username'] is None:
            raise ValueError("Missing username in credentials.")

        return authconfig

    def find_device_from_config (self, search, driver=None, credentials=None):

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
                if not driver:
                    driver = d['driver']

                if not credentials:
                    credentials = d['credentials']

                host_result = hostname

                # Found first entry, no need to carry on.
                break

        # If we get here both credentials and driver should be set either from
        # the config file or passed as parameters

        if not driver:
            raise ValueError('Can not find driver for host {}, try with driver parameter.'.format(host_result))

        if not credentials:
            raise ValueError('Can not find credentials for host {}, try with credentials parameter.'.format(host_result))

        if driver not in ["ios", "iosxr", "junos", "eos", "fortios", "ibm", "nxos", "pluribus", "panos", "ros", "vyos"]:
            raise ValueError('Driver "{}" is not a valid NAPALM Driver.'.format(driver))

        # Return, this will be the original search if we didn't find anything
        #
        return (host_result, driver, credentials)
