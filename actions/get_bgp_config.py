from lib.action import NapalmBaseAction


class NapalmGetBGPConfig(NapalmBaseAction):
    """Get BGP configuration from a network device via NAPALM
    """

    def run(self, group, neighbour, htmlout=False, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:

                if not group:
                    if not neighbour:
                        bgpconf = device.get_bgp_config()
                    else:
                        bgpconf = device.get_bgp_config(neighbor=neighbour)
                else:
                    if not neighbour:
                        bgpconf = device.get_bgp_config(group=group)
                    else:
                        bgpconf = device.get_bgp_config(group=group, neighbor=neighbour)

                result = {'raw': bgpconf}

                if htmlout:
                    result['html'] = self.html_out(result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
