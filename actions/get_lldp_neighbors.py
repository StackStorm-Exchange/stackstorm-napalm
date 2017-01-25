from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetLLDPNeighbours(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, interface):

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


                if not neighbour:
                    lldp_neighbours = device.get_lldp_neighbors()
                else:
                    lldp_neighbours = device.get_lldp_neighbors_detail(interface)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, lldp_neighbours)
