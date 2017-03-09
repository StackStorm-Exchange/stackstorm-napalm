from lib.action import NapalmBaseAction


class NapalmCLI(NapalmBaseAction):
    """Run CLI commands on a network device via NAPALM
    """

    def run(self, commands, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:
                cmds_output = device.cli(commands)

                result = {'raw': cmds_output}

                result_with_pre = {}
                result_as_array = {}

                for this_cmd in cmds_output:
                    result_as_array[this_cmd] = cmds_output[this_cmd].split('\n')
                    if self.htmlout:
                        result_with_pre[this_cmd] = "<pre>" + cmds_output[this_cmd] + "</pre>"

                result['raw_array'] = result_as_array

                if self.htmlout:
                    result['html'] = self.html_out(result_with_pre)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
