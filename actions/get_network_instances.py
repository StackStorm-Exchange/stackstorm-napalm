from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetNetworkInstances(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, name):

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

                if not name:
                    network_instances = device.get_network_instances()
                else:
                    network_instances = device.get_network_instances(name)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, network_instances)
