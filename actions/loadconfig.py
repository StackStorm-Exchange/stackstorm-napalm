from lib.action import NapalmBaseAction


class NapalmLoadConfig(NapalmBaseAction):
    """Load configuration into network device via NAPALM
    """

    def run(self, config_file, method, inline_transfer, **std_kwargs):

        if not method:
            method = 'merge'
        else:
            method = method.lower()
            if method not in ["merge", "replace"]:
                raise ValueError(('{} is not a valid load method, use: '
                                  'merge or replace').format(method))

        with self.get_driver(**std_kwargs) as device:
            # inline_transfer: If set it becomes True, else False
            device.inline_transfer = inline_transfer

            if method == "replace":
                device.load_replace_candidate(filename=config_file)
            else:
                device.load_merge_candidate(filename=config_file)

            device.commit_config()

        return (True, "load ({}) successful on {}".format(method, self.hostname))
