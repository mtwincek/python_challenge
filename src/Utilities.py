import logging
import re
log = logging.getLogger(__name__)


def is_valid_ip_address(ip_address):
    for value in ip_address.split("."):
        if not (0 <= int(value) < 256):
            log.debug("IP Address \"%s\" is not valid" % ip_address)
            return False
    log.debug("IP Address \"%s\" is valid" % ip_address)
    return True


def get_keys_recursively(item_to_traverse):
    set_of_keys = set()
    if isinstance(item_to_traverse, dict):
        for key, value in item_to_traverse.items():
            log.debug("Found key \"%s\"" % key)
            set_of_keys.add(key)
            set_of_keys = set_of_keys.union(get_keys_recursively(value))
    elif isinstance(item_to_traverse, list):
        for item in item_to_traverse:
            set_of_keys = set_of_keys.union(get_keys_recursively(item))
    else:
        pass
    return set_of_keys


def get_search_recursively(item_to_traverse, search_dictionary, previous_key=None):
    search_param_pass = {key: False for key in search_dictionary}
    if isinstance(item_to_traverse, dict):
        for key, value in item_to_traverse.items():
            search_param_pass = disjunction_dictionary(search_param_pass, get_search_recursively(value, search_dictionary, key))
    elif isinstance(item_to_traverse, list):
        for item in item_to_traverse:
            search_param_pass = disjunction_dictionary(search_param_pass, get_search_recursively(item, search_dictionary, previous_key))
    else:
        if previous_key in search_dictionary:
            if re.search(search_dictionary[previous_key].replace("*", ".*"), str(item_to_traverse), re.DOTALL) is not None:
                search_param_pass[previous_key] = True
    return search_param_pass


def disjunction_dictionary(dict_1, dict_2):
    return_dict = {key: False for key in dict_1}
    for key in dict_1.keys():
        if dict_1[key] or dict_2[key]:
            return_dict[key] = True
    return return_dict


def is_dict_all_true(dict_var):
    for value in dict_var.values():
        if not value:
            return False
    return True

