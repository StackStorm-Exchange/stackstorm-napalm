from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetLog(NapalmBaseAction):

    def run(self, hostname, host_ip, driver, port, credentials, lastlines, htmlout=False):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname, host_ip, driver, credentials) = self.find_device_from_config(hostname, host_ip, driver, credentials)

            login = self._get_credentials(credentials)

            if not lastlines:
                lastlines = 5

            if driver == 'junos':
                log_cmd = 'show log messages'
                commands = ['set cli screen-width 0', 'set cli screen-length 0']
                commands.append(log_cmd)
            elif driver == 'iosxr':
                log_cmd = 'show log'
                commands = ['term width 0', 'term len 0']
                commands.append(log_cmd)
            elif driver == 'ios':
                log_cmd = 'show log'
                commands = ['term width 0', 'term len 0']
                commands.append(log_cmd)
            elif driver == 'eos':
                log_cmd = 'show log'
                commands = ['term width 32767', 'term len 0']
                commands.append(log_cmd)
            else:
                raise ValueError('Not able to find logging command for {}, with driver {}.'.format(hostname, driver))

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
                cmd_result = device.cli(commands)
                log_output = list(filter(None, cmd_result[log_cmd].split('\n')))
                result = {"raw" : log_output[-lastlines:] }

            if htmlout:
                result['html'] = "<pre>" + result['raw'].join("\n") + "</pre>"

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
