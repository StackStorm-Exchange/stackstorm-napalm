from lib.action import NapalmBaseAction


class NapalmGetLog(NapalmBaseAction):
    """Get Logs from a network device via NAPALM
    """

    def run(self, lastlines, htmlout=False, **std_kwargs):

        try:

            if not lastlines:
                lastlines = 5

            if self.driver == 'junos':
                log_cmd = 'show log messages'
                commands = ['set cli screen-width 0', 'set cli screen-length 0']
                commands.append(log_cmd)
            elif self.driver == 'iosxr':
                log_cmd = 'show log'
                commands = ['term width 0', 'term len 0']
                commands.append(log_cmd)
            elif self.driver == 'ios':
                log_cmd = 'show log'
                commands = ['term width 0', 'term len 0']
                commands.append(log_cmd)
            elif self.driver == 'eos':
                log_cmd = 'show log'
                commands = ['term width 32767', 'term len 0']
                commands.append(log_cmd)
            else:
                raise ValueError(('Not able to find logging command for {}, '
                                  'with driver {}.').format(self.hostname, self.driver))

            with self.get_driver(**std_kwargs) as device:
                cmd_result = device.cli(commands)
                log_output = list(filter(None, cmd_result[log_cmd].split('\n')))
                result = {"raw": log_output[-lastlines:]}

            if htmlout:
                result['html'] = "<pre>" + "\n".join(result['raw']) + "</pre>"

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
