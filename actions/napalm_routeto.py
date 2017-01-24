from napalm import get_network_driver

from st2actions.runners.pythonrunner import Action


class NapalmRouteTo(Action):
    """Load configuration into network device via NAPALM
    """
    def __init__(self, *args, **kwargs):
        super(NapalmRouteTo, self).__init__(*args, **kwargs)

    def run(self, driver, hostname, username, password, port, destination, protocol):


        with get_network_driver(driver)(
            hostname=str(hostname),
            username=username,
            password=password,
            optional_args={'port': str(port)}
        ) as device:

            route = device.get_route_to(destination, protocol)

        return (TRUE, route)
