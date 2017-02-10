from napalm import get_network_driver

from lib.action import NapalmBaseAction


class NapalmGetProbesConfig(NapalmBaseAction):
    """Get IP SLA probe config from a network device via NAPALM
    """

    def run(self, hostname, host_ip, driver, port, credentials, htmlout=False):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname,
             host_ip,
             driver,
             credentials) = self.find_device_from_config(hostname, host_ip, driver, credentials)

            if driver not in ["iosxr", "junos"]:
                raise ValueError(('Not supported with {} driver, only IOS-XR and JunOS '
                                  'are supported.').format(driver))

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
                result = {'raw': device.get_probes_config()}

                if htmlout:
                    result['html'] = self.html_out(result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
