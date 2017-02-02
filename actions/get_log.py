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
            raise ValueError('Can not find driver for host {}, try with driver parameter.'.format(hostname))

        if not credentials:
            raise ValueError('Can not find credentials for host {}, try with credentials parameter.'.format(hostname))

        login = self._get_credentials(credentials)

        if not lastlines:
            lastlines = '5'
        else:
            lastlines = str(lastlines)

        if driver == 'junos':
            log_cmd = 'show log messages | last  ' + lastlines
            commands = ['set cli screen-width 0', 'set cli screen-length 0']
            commands.append(log_cmd)
        elif driver == 'iosxr':
            log_cmd = 'show log last  ' + lastlines
            commands = ['term width 0', 'term len 0']
            commands.append(log_cmd)
        elif driver == 'ios':
            log_cmd = 'show log'
            commands = ['term width 0', 'term len 0']
            commands.append(log_cmd)
        elif driver == 'eos':
            log_cmd = 'show log ' + lastline
            commands = ['term width 32767', 'term len 0']
            commands.append(log_cmd)
        else:
            raise ValueError('Not able to find logging command for {}, with driver {}.'.format(hostname, driver))

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
                cmd_result = device.cli(commands)
                result = cmd_result[log_cmd]

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
