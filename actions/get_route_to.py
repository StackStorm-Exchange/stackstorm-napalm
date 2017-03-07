from lib.action import NapalmBaseAction


class NapalmGetRouteTo(NapalmBaseAction):
    """Get route from a network device via NAPALM
    """

    def run(self, destination, protocol, htmlout=False, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:

                if not protocol:
                    route = {'raw': device.get_route_to(destination)}
                else:
                    route = {'raw': device.get_route_to(destination, protocol)}

                if htmlout:
                    route['html'] = self.html_out(route['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, route)
