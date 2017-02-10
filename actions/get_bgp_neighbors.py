from napalm import get_network_driver

from lib.action import NapalmBaseAction


class NapalmGetBGPNeighbours(NapalmBaseAction):
    """Get BGP Neighbours from a network device via NAPALM
    """

    def run(self, hostname, host_ip, driver, port, credentials, routing_instance, neighbour, htmlout=False):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname,
             host_ip,
             driver,
             credentials) = self.find_device_from_config(hostname, host_ip, driver, credentials)

            login = self.get_credentials(credentials)

            if not port:
                optional_args = None
            else:
                optional_args = {'port': str(port)}

            with get_network_driver(driver)(
                hostname=str(host_ip),
                username=login['username'],
                password=login['password'],
                optional_args=optional_args
            ) as device:
                result = device.get_bgp_neighbors()

                if routing_instance not in result:
                    raise ValueError(('Routing instance {} does not exist on '
                                      'this device.').format(routing_instance))

                if not neighbour:
                    bgp_neighbours = result[routing_instance]['peers']
                else:
                    if neighbour not in result[routing_instance]['peers']:
                        raise ValueError(('BGP Neighbour {} does not exist '
                                          'on this device.').format(neighbour))
                    else:
                        bgp_neighbours = result[routing_instance]['peers'][neighbour]

                result = {'raw': bgp_neighbours}

                if htmlout:
                    result['html'] = self.html_out(result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
