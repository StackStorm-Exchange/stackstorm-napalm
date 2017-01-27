from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetBGPConfig(NapalmBaseAction):

    def run(self, hostname, driver, port, credentials, group, neighbour):

        login = self._get_credentials(credentials)

        # Look up the driver if it's not given from the configuration file
        # Also overides the hostname since we might have a partial host i.e. from
        # syslog such as host1 instead of host1.example.com
        #
        if not driver:
            (hostname, driver) = self.find_device_from_config(hostname)

            if not driver:
                raise ValueError(('Can not find driver for host %s, try with driver parameter.' % (hostname)))


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
