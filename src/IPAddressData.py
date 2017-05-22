import logging
import re
import requests
import src.Utilities as Utilities
log = logging.getLogger(__name__)


class IPAddressDataList(object):
    def __init__(self):
        self.ip_address_data_list = list()       # list of class IPAddressData
        self.search_keys = set()                 # set of strings

    def parse_ips_from_file(self, file_name):
        log.debug("Running function \"%s\"" % self.parse_ips_from_file.__name__)
        set_of_ip_address = set()
        with open(file_name, 'r') as open_file:
            # Find each ip address in line
            for line in open_file:
                found_ip_address_list = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
                # Put each ip address into a set to avoid duplicates
                for found_ip_address in found_ip_address_list:
                    log.debug("Potential IP Address \"%s\" found" % found_ip_address)
                    # Validate ip address
                    if Utilities.is_valid_ip_address(found_ip_address):
                        set_of_ip_address.add(found_ip_address)
        # Input sorted set of ip addresses into list of IPAddressData
        for ip_address in sorted(set_of_ip_address):
            self.ip_address_data_list.append(IPAddressData(ip_address))

    def get_string_of_ip_address_data_list(self):
        return '\n'.join(str(item.ip_data) for item in self.ip_address_data_list)

    def get_api_data(self, template_query_link):
        log.debug("Running function \"%s\"" % self.get_api_data.__name__)
        for item_ip_data in self.ip_address_data_list:
            query_link = template_query_link % item_ip_data.ip_address
            log.debug("Requesting from \"%s\"" % query_link)
            response_from_query = requests.get(query_link)
            if response_from_query.status_code == 200:
                response_as_dict = response_from_query.json()
                item_ip_data.ip_data.update(response_as_dict)
            else:
                log.warning("Query of \"%s\" failed to respond properly... skipping" % template_query_link)

    def get_ip_data_keys(self):
        set_of_keys = set()
        for item in self.ip_address_data_list:
            set_of_keys = set_of_keys.union(Utilities.get_keys_recursively(item.ip_data))
        self.search_keys = sorted(self.search_keys.union(set_of_keys))

    def get_ip_data(self, cmp_ip_address):
        for item in self.ip_address_data_list:
            if item.ip_address == cmp_ip_address:
                return item.ip_data
        return None

    def get_list_of_ip_addresses(self):
        return '\n'.join(str(item.ip_address) for item in self.ip_address_data_list)

    def get_ip_address_with_search_parameters(self, search_dictionary):
        ip_addresses_that_match = list()
        for item in self.ip_address_data_list:
            if Utilities.is_dict_all_true(Utilities.get_search_recursively(item.ip_data, search_dictionary, None)):
                ip_addresses_that_match.append(item.ip_address)
        return '\n'.join(str(item) for item in ip_addresses_that_match)


class IPAddressData(object):
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.ip_data = dict()
