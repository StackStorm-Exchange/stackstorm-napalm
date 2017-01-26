from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetBGPNeighbours(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, neighbour):

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

                if not neighbour:
                    bgp_neighbours = device.get_bgp_neighbors()
                else:
                    bgp_neighbours = device.get_bgp_neighbors_detail(neighbour)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, bgp_neighbours)
