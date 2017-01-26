from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmTraceroute(NapalmBaseAction):

    def run(self, driver, hostname, port, credentials, destination, source=u'', ttl=255, trtimeout=2):

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

                route = device.traceroute(destination, source, ttl, trtimeout)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, route)
