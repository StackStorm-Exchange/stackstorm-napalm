from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetNTP(NapalmBaseAction):

    def run(self, hostname, host_ip, driver, port, credentials, type):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname, host_ip, driver, credentials) = self.find_device_from_config(hostname, host_ip, driver, credentials)

            login = self._get_credentials(credentials)

            if not type:
                type = 'stats'
            else:
                type = type.lower()
                if type not in ["stats", "servers", "peers"]:
                    raise ValueError (("%s is not a valid ntp query type, use: stats, servers or peers" % (type)))

            if not port:
                optional_args=None
            else:
                optional_args={'port': str(port)}

            with get_network_driver(driver)(
                hostname=str(host_ip),
                username=login['username'],
                password=login['password'],
                optional_args=optional_args
            ) as device:

                if type == "stats":
                    ntp_result = device.get_ntp_stats()
                elif type == "servers":
                    ntp_result = device.get_ntp_servers()
                elif type == "peers":
                    ntp_result = device.get_ntp_peers()
                else:
                    raise ValueError (("%s is not a valid ntp query type, use: stats, servers or peers" % (type)))

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, ntp_result)
