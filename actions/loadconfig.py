from lib.action import NapalmBaseAction


class NapalmLoadConfig(NapalmBaseAction):
    """Load configuration into network device via NAPALM
    """

    def run(self, config_file, config_text, method, inline_transfer, **std_kwargs):
        if not config_file and not config_text:
            raise ValueError('Specify either config_file or config_text')

        with self.get_driver(**std_kwargs) as device:
            # inline_transfer: If set it becomes True, else False
            device.inline_transfer = inline_transfer

            if method == "replace":
                device.load_replace_candidate(filename=config_file, config=config_text)
            else:
                device.load_merge_candidate(filename=config_file, config=config_text)

            device.commit_config()

        return (True, "load ({}) successful on {}".format(method, self.hostname))
