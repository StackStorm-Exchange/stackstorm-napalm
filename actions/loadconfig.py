from napalm import get_network_driver

from lib.action import NapalmBaseAction


class NapalmLoadConfig(NapalmBaseAction):
    """Load configuration into network device via NAPALM
    """

    def run(self, hostname, host_ip, driver, port, credentials, config_file, method):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname,
             host_ip,
             driver,
             credentials) = self.find_device_from_config(hostname, host_ip, driver, credentials)

            login = self.get_credentials(credentials)

            if not method:
                method = 'merge'
            else:
                method = method.lower()
                if method not in ["merge", "replace"]:
                    raise ValueError(('{} is not a valid load method, use: '
                                      'merge or replace').format(method))

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

                if method == "replace":
                    device.load_replace_candidate(filename=config_file)
                else:
                    device.load_merge_candidate(filename=config_file)

                device.commit_config()

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, "load ({}) successful on {}".format(method, hostname))
