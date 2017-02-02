from napalm import get_network_driver

from lib.action import NapalmBaseAction


class NapalmLoadConfig(Action):
    """Load configuration into network device via NAPALM
    """

    def run(self, hostname, driver, port, credentials, config_file, method):

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

        # Usually I'd rely on setting the "method" arg for this function as an optional arg, but
        # that doesn't seem to work - I'm guessing the caller for this function is actually calling
        # this function with method set to "None" if the action is omitting this arg

        try:
            if not method:
                method = 'merge'
            else:
                method = method.lower()
                if method not in ["merge", "replace"]:
                    raise ValueError (("%s is not a valid load method, use: merge or replace" % (method)))

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

                if method == "replace":
                    device.load_replace_candidate(
                        filename=config_file
                    )
                else:
                    device.load_merge_candidate(
                        filename=config_file
                    )

                device.commit_config()

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, ("load (%s) successful on %s" % (method, hostname)))
