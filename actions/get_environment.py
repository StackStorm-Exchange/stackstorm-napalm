from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetEnv(NapalmBaseAction):

    def run(self, hostname, driver, port, credentials):

        login = self._get_credentials(credentials)

        try:

            if not port:
                optional_args=None
            else:
                optional_args={'port': str(port)}

            with get_network_driver(driver)(
                hostname=str(hostname),
                username=login['username'],
                password=login['password'],
                optional_args=optional_args
            ) as device:
                result = device.get_environment()

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
