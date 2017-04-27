from lib.action import NapalmBaseAction


class NapalmGetBGPConfig(NapalmBaseAction):
    """Get BGP configuration from a network device via NAPALM
    """

    def run(self, group, neighbor, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:

                if not group:
                    if not neighbor:
                        bgpconf = device.get_bgp_config()
                    else:
                        bgpconf = device.get_bgp_config(neighbor=neighbor)
                else:
                    if not neighbor:
                        bgpconf = device.get_bgp_config(group=group)
                    else:
                        bgpconf = device.get_bgp_config(group=group, neighbor=neighbor)

                result = {'raw': bgpconf}

                if self.htmlout:
                    result['html'] = self.html_out(result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
