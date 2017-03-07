from lib.action import NapalmBaseAction


class NapalmTraceroute(NapalmBaseAction):
    """Run a tracroute from a network device via NAPALM
    """

    def run(self, destination, source, ttl=255, trtimeout=2, htmlout=False, **std_kwargs):

        try:
            with self.get_driver(**std_kwargs) as device:

                result = {'raw': device.traceroute(destination, source, ttl, trtimeout)}

                if htmlout:
                    result['html'] = self.html_out(result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, result)
