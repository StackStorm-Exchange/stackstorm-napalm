from napalm import get_network_driver

from st2actions.runners.pythonrunner import Action


class NapalmLoadConfig(Action):
    """Load configuration into network device via NAPALM
    """
    def __init__(self, *args, **kwargs):
        super(NapalmLoadConfig, self).__init__(*args, **kwargs)

    def run(self, driver, hostname, username, password, port, config, method="merge"):

        # Need to determine the best way to GET the config to put on
        # the device. You currently just require the text, but maybe they
        # want to give a file.
        # Maybe they want to give a git repository.....

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
                    filename='test/unit/eos/new_good.conf'
                )
            else:
                device.load_merge_candidate(
                    config='interface Ethernet2\ndescription bla'
                )

        return "load (%s) successful on %s" % (method, hostname)
