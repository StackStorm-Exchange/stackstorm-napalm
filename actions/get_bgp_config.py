from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetBGPConfig(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, group, neighbour):

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

                if not group:
                    if not neighbour:
                        bgpconf = device.get_bgp_config()
                    else:
                        bgpconf = device.get_bgp_config(neighbor=neighbour)
                else:
                    if not neighbour:
                        bgpconf = device.get_bgp_config(group=group)
                    else:
                        bgpconf = device.get_bgp_config(group=group, neighbor=neighbour)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, bgpconf)
