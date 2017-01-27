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
            raise ValueError(('Can not find credentials group "%s". ' % (credentials)))

        if authconfig['password'] is None:
            raise ValueError("Missing password in credentials.")

        if authconfig['username'] is None:
            raise ValueError("Missing username in credentials.")

        return authconfig

    def find_driver_for_device (self, hostname):

        devices = self.config['devices']

        for d in devices:
            if d['hostname'] == hostname:
                return d
