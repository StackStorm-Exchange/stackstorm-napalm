from lib.action import NapalmBaseAction


class NapalmGetNTP(NapalmBaseAction):
    """Get NTP details from a network device via NAPALM
    """

    def run(self, query_type, htmlout=False, **std_kwargs):

        try:
            if not query_type:
                query_type = 'stats'
            else:
                query_type = type.lower()
                if query_type not in ["stats", "servers", "peers"]:
                    raise ValueError(('{} is not a valid ntp query type use: '
                                      'stats, servers or peers.').format(query_type))

            with self.get_driver(**std_kwargs) as device:

                if type == "stats":
                    ntp_result = {'raw': device.get_ntp_stats()}
                elif type == "servers":
                    ntp_result = {'raw': device.get_ntp_servers()}
                elif type == "peers":
                    ntp_result = {'raw': device.get_ntp_peers()}
                else:
                    raise ValueError(('{} is not a valid ntp query type use: '
                                      'stats, servers or peers.').format(type))

                if htmlout:
                    ntp_result['html'] = self.html_out(ntp_result['raw'])

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, ntp_result)
