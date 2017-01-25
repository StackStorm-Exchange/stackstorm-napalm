from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetInterfaces(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, counters, ipaddresses):

        login = self._get_credentials(credentials)

        try:

            if counters and ipaddresses:
                raise ValueError("Both ipaddresses and counters can not be set at the same time.")

            if not port:
                port = 22

            with get_network_driver(driver)(
                hostname=str(hostname),
                username=login['username'],
                password=login['password'],
                optional_args={'port': str(port)}
            ) as device:
                self.logger.info(('Successfully connected to device "%s". ' % (hostname)))

                if counters:
                    interfaces = device.get_interfaces_counters()
                elif ipaddresses:
                    interfaces = device.get_interfaces_ip()
                else:
                    interfaces = device.get_interfaces()

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, interfaces)
