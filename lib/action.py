from napalm import get_network_driver

from st2actions.runners.pythonrunner import Action


class NapalmBaseAction(Action):

    def __init__(self, config):
        super(NapalmBaseAction, self).__init__(config)

    def _get_credentials(self, credentials):

        authconfig = self.config['credentials'].get(credentials, None)

        if not authconfig:
            raise ValueError(('Invalid credentials set name "%s". Please make'
                              ' sure that credentials set with this name is'
                              ' defined in the config' % (credentials)))

        if authconfig['password'] is None:
            raise ValueError("Missing password in credentials.")

        if authconfig['username'] is None:
            raise ValueError("Missing username in credentials.")

        return authconfig
