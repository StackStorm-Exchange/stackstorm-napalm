from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetConfig(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, retrieve):

        login = self._get_credentials(credentials)

        try:

            if not port:
                port = 22

            with get_network_driver(driver)(
                hostname=str(hostname),
                username=login['username'],
                password=login['password'],
                optional_args={'port': str(port)}
            ) as device:

                if not retrieve:
                    config_output = device.get_config()
                else:
                    config_output = device.get_config(retrieve)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, config_output)
