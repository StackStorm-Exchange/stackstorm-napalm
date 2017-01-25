from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmRouteTo(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, destination, protocol):

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
                route = device.get_route_to(destination, protocol)

        except Exception, e:
            self.logger.error(str(e))
            return False

        return (True, route)
