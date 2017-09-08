from lib.action import NapalmBaseAction


class NapalmGetFirewallPolicies(NapalmBaseAction):
    """Get Firewall Policies from a network device via NAPALM
    """

    def run(self, **std_kwargs):

        with self.get_driver(**std_kwargs) as device:
            result = {'raw': device.get_firewall_policies()}

            if self.htmlout:
                result['html'] = self.html_out(result['raw'])

        return (True, result)
