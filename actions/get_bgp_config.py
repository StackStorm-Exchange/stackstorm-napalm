from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetBGPConfig(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, group, neighbour):

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
                self.logger.info(('Successfully connected to device "%s". ' % (hostname)))

                if not group:
                    route = device.get_bgp_config()
                else:
                    route = device.get_route_to(group, neighbour)

        except Exception, e:
            self.logger.error(str(e))
            return False

        return (True, route)
