from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetFirewallPolicies(NapalmBaseAction):

	def run(self, hostname, driver, port, credentials):

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
				result = device.get_firewall_policies()

		except Exception, e:
			self.logger.error(str(e))
			return (False, str(e))

		return (True, result)
