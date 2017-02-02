from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetLog(NapalmBaseAction):

    def run(self, hostname, driver, port, credentials, lastlines):

        # Look up the driver  and if it's not given from the configuration file
        # Also overides the hostname since we might have a partial host i.e. from
        # syslog such as host1 instead of host1.example.com
        #
        (hostname, driver, credentials) = self.find_device_from_config(hostname, driver, credentials)

        if not driver:
            raise ValueError(('Can not find driver for host %s, try with driver parameter.' % (hostname)))

        if not credentials:
            raise ValueError(('Can not find credentials for host %s, try with credentials parameter.' % (hostname)))

        login = self._get_credentials(credentials)

        if not lastlines:
            lastlines = 50;

        if driver == 'junos':
            commands = ['set cli screen-width 0', 'set cli screen-length 0', 'show log messages | last  ' . lastlines]
        elif driver == 'iosxr':
            commands = ['term width 0', 'term len 0', 'show log last ' . lastlines]
        elif driver == 'ios':
            commands = ['term width 0', 'term len 0', 'show log']
        elif driver == 'eos':
            commands = ['term width 32767', 'term len 0', 'show log ' . lastline]
        else:
            raise ValueError(('Not able to find logging command for %s, with driver %s.' % (hostname, driver)))

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
                result = device.cli(commands)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
