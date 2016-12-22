from napalm import get_network_driver

from st2actions.runners.pythonrunner import Action


class NapalmLoadConfig(Action):
    """Load configuration into network device via NAPALM
    """
    def __init__(self, *args, **kwargs):
        super(NapalmLoadConfig, self).__init__(*args, **kwargs)

    def run(self, driver, hostname, username, password, port, config_file, method):

        # Usually I'd rely on setting the "method" arg for this function as an optional arg, but
        # that doesn't seem to work - I'm guessing the caller for this function is actually calling
        # this function with method set to "None" if the action is omitting this arg
        if not method:
            method = 'merge'
        else:
            method = method.lower()
            if method not in ["merge", "replace"]:
                raise ValueError

        with get_network_driver(driver)(
            hostname=str(hostname),
            username=username,
            password=password,
            optional_args={'port': str(port)}
        ) as device:

            if method == "replace":
                device.load_replace_candidate(
                    filename=config_file
                )
            else:
                device.load_merge_candidate(
                    filename=config_file
                )

        return "load (%s) successful on %s" % (method, hostname)
