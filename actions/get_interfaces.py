from lib.action import NapalmBaseAction


class NapalmGetInterfaces(NapalmBaseAction):
    """Get Interfaces from a network device via NAPALM
    """

    def run(self, interface=None, counters=False, ipaddresses=False, **std_kwargs):

        try:

            if counters and ipaddresses:
                raise ValueError("Both ipaddresses and counters can not be set at the same time.")

            with self.get_driver(**std_kwargs) as device:

                if counters:
                    result = device.get_interfaces_counters()
                elif ipaddresses:
                    result = device.get_interfaces_ip()
                else:
                    result = device.get_interfaces()

                if interface:
                    interfaces = {"raw": result.get(interface)}
                    interfaces['raw']['name'] = interface
                else:
                    interfaces = {"raw": result}

                if self.htmlout:
                    interfaces['html'] = self.html_out(interfaces['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, interfaces)
