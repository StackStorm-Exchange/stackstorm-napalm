from napalm import get_network_driver
from json2html import *

from lib.action import NapalmBaseAction

class NapalmGetInterfaces(NapalmBaseAction):

    def run(self, hostname, host_ip, driver, port, credentials, interface=None, counters=False, ipaddresses=False, htmlout=False):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname, host_ip, driver, credentials) = self.find_device_from_config(hostname, host_ip, driver, credentials)

            login = self._get_credentials(credentials)

            if counters and ipaddresses:
                raise ValueError("Both ipaddresses and counters can not be set at the same time.")

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

                if counters:
                    result = device.get_interfaces_counters()
                elif ipaddresses:
                    result = device.get_interfaces_ip()
                else:
                    result = device.get_interfaces()

                if interface:
                    interfaces = result.get(interface)
                    interfaces['name'] = interface
                else:
                    interfaces = result

                if htmlout:
                    interfaces = json2html.convert(json = interfaces)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, interfaces)
