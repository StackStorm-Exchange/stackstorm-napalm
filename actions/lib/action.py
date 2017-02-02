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

                return (d['hostname'], driver, credentials)

        # Return the original search if we don't find anything
        #
        return (search, driver, credentials)
