from lib.action import NapalmBaseAction


class NapalmGetConfig(NapalmBaseAction):

    def run(self, retrieve, **std_kwargs):

        with self.get_driver(**std_kwargs) as device:

            if not retrieve:
                config_output = device.get_config()
            else:
                config_output = device.get_config(retrieve)

            result = {'raw': config_output}
            if self.htmlout:
                result['html'] = self.html_out(result['raw'])

        return (True, result)
