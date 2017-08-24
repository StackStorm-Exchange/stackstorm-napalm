from lib.action import NapalmBaseAction


class NapalmGetEnv(NapalmBaseAction):
    """Get Environment details from a network device via NAPALM
    """

    def run(self, **std_kwargs):

        with self.get_driver(**std_kwargs) as device:
            result = {'raw': device.get_environment()}

            if self.htmlout:
                result['html'] = self.html_out(result['raw'])

        return (True, result)
