from napalm import get_network_driver

from lib.action import NapalmBaseAction


class NapalmCLI(NapalmBaseAction):
    """Run CLI commands on a network device via NAPALM
    """

    def run(self, hostname, host_ip, driver, port, credentials, commands, htmlout=False):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname, host_ip, driver, credentials) = self.find_device_from_config(hostname, host_ip, driver, credentials)

            login = self._get_credentials(credentials)

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
                cmds_output = device.cli(commands)

               result = {'raw' : cmds_output }

                result_with_pre = {}
                result_as_array = {}

                for this_cmd in cmds_output:
                    result_as_array[this_cmd] = cmds_output[this_cmd].split('\n')
                    if htmlout:
                      result_with_pre[this_cmd] = "<pre>" + cmds_output[this_cmd] + "</pre>"

                result['raw_array'] = result_as_array

                if htmlout:
                    result['html'] = self._html_out(result_with_pre)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
