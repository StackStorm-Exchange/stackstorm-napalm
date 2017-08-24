from lib.action import NapalmBaseAction


class NapalmGetProbesConfig(NapalmBaseAction):
    """Get IP SLA probe config from a network device via NAPALM
    """

    def run(self, **std_kwargs):

        if self.driver not in ["iosxr", "junos"]:
            raise ValueError(('Not supported with {} driver, only IOS-XR and JunOS '
                              'are supported.').format(self.driver))

        with self.get_driver(**std_kwargs) as device:
            result = {'raw': device.get_probes_config()}

            if self.htmlout:
                result['html'] = self.html_out(result['raw'])

        return (True, result)
