from lib.action import NapalmBaseAction


class NapalmGetConfig(NapalmBaseAction):

    def run(self, retrieve, htmlout=False, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:

                if not retrieve:
                    config_output = device.get_config()
                else:
                    config_output = device.get_config(retrieve)

                result = {'raw': config_output}
                if htmlout:
                    result['html'] = self.html_out(result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
