from lib.action import NapalmBaseAction


class NapalmGetLog(NapalmBaseAction):
    """Get logs from a network device via NAPALM
    """

    def run(self, lastlines=5, **std_kwargs):

        cmd_dict = {
            "junos": {
                "log_cmd": "show log messages",
                "commands": ['set cli screen-width 0', 'set cli screen-length 0']
            },
            "iosxr": {
                "log_cmd": "show log",
                "commands": ['term width 0', 'term len 0']
            },
            "ios": {
                "log_cmd": "show log",
                "commands": ['term width 0', 'term len 0']
            },
            "eos": {
                "log_cmd": "show log",
                "commands": ['term width 32767', 'term len 0']
            },
        }

        with self.get_driver(**std_kwargs) as device:

            try:
                log_cmd = cmd_dict[self.driver]["log_cmd"]
                commands = cmd_dict[self.driver]["commands"]
                commands.append(log_cmd)
            except KeyError:
                self.logger.error('Not able to find logging command for {}, '
                                  'with driver {}.').format(self.hostname, self.driver)
                raise

            cmd_result = device.cli(commands)
            log_output = list(filter(None, cmd_result[log_cmd].split('\n')))
            result = {"raw": log_output[-lastlines:]}

        if self.htmlout:
            result['html'] = "<pre>" + "\n".join(result['raw']) + "</pre>"

        return (True, result)
