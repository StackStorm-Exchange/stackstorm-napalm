from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetBGPNeighbours(NapalmBaseAction):

    def run(self, hostname, driver, port, credentials, routing_instance, neighbour):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname, driver, credentials) = self.find_device_from_config(hostname, driver, credentials)

            login = self._get_credentials(credentials)
            
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
                result = device.get_bgp_neighbors()

                if routing_instance not in result:
                    raise ValueError('Routing instance {} does not exist on this device.'.format(routing_instance))

                if not neighbour:
                    bgp_neighbours = result[routing_instance]['peers']
                else:
                    if neighbour not in result[routing_instance]['peers']:
                        raise ValueError('BGP Neighbour {} does not exist on this device.'.format(neighbour))
                    else:
                        bgp_neighbours = result[routing_instance]['peers'][neighbour]

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, bgp_neighbours)
