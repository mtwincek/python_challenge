import logging
import os
from src.IPAddressData import IPAddressDataList
log = logging.getLogger(__name__)


def ip_address_processor(file_input):
    try:
        log.debug("Running function \"%s\"" % ip_address_processor.__name__)
        # Setup object to hold all ip addresses and related data
        ip_list_obj = IPAddressDataList()

        # Process input file
        ip_list_obj.parse_ips_from_file(file_input)

        # Add data from Geo IP
        # Example link: "http://freegeoip.net/json/40.82.106.5"
        ip_list_obj.get_api_data("http://freegeoip.net/json/%s")

        # Add data from RDAP
        # Example link: "http://rdap.apnic.net/ip/40.82.106.5"
        ip_list_obj.get_api_data("http://rdap.apnic.net/ip/%s")

        # Determine keys
        ip_list_obj.get_ip_data_keys()

        # Query results
        response = str()
        while response != "exit":
            #######################################
            # Print main screen
            #######################################
            os.system('clear')
            print("Potential keys to search:")
            print("   \"" + '\"\n   \"'.join(str(item) for item in ip_list_obj.search_keys) + "\"")
            print("\n USAGE:")
            print("   list                   --   get list of ip addresses")
            print("   ipdata=<ip address>    --   get ip data for given ip address")
            print("   search=<key>:<value>   --   search for ip address that match value on a key")
            print("   exit                   --   exit program\n")
            print("EXAMPLES:")
            print("   list")
            print("   ipdata=40.82.106.5")
            print("   search=\"ip\":\"40.82.106.5\"")
            print("   search=\"ip\":\"40.82.106.5\",\"city\":\"Amsterdam\"")
            print("   search=\"ip\":\"40.82.106.5\",\"city\":\"Amster*\"")
            print("   exit\n")
            response = input("Enter command: ")
            #######################################
            # Command "exit"
            #######################################
            if response == "exit":
                print("Exiting")
                raise SystemExit
            #######################################
            # Command for other input
            #######################################
            else:
                command_type = response.split("=", 1)
                valid_command = False
                results = None
                #######################################
                # Command "list"
                #######################################
                if command_type[0] == "list":
                    valid_command = True
                    results = ip_list_obj.get_list_of_ip_addresses()
                #######################################
                # Command "ipdata"
                #######################################
                elif command_type[0] == "ipdata":
                    if len(command_type) == 2:
                        valid_command = True
                        results = ip_list_obj.get_ip_data(command_type[1])
                #######################################
                # Command "search"
                #######################################
                elif command_type[0] == "search":
                    search_dictionary = validate_search_command(command_type)
                    if search_dictionary is not None:
                        valid_command = True
                        results = ip_list_obj.get_ip_address_with_search_parameters(search_dictionary)
                #######################################
                # Results of command or invalid command
                #######################################
                # os.system('clear')
                print("Command: %s" % response)
                if not valid_command:
                    print("Invalid command")
                else:
                    print("\nRESULTS:")
                    print(results)
            input("\n\n\nPress ENTER key...")

        # DEBUG TEST
        # print(ip_list_obj.get_string_of_ip_address_data_list())
    except Exception as exc_err:
        log.exception(str(exc_err))
        raise SystemExit


def validate_search_command(command_type):
    search_dictionary = dict()
    if len(command_type) == 2:
        search_parameters = command_type[1]
        # Validate that key starts with and value ends with quote symbol (")
        if search_parameters[0] == "\"" and search_parameters[-1]:
            # Strip quotes at beginning and end
            search_parameters = search_parameters[1:-1]
            # Separate each search parameter
            list_of_search_parameters = search_parameters.split("\",\"")
            # Get each key and search value
            for item in list_of_search_parameters:
                # Separate key and search value
                key_value = item.split("\":\"")
                # Check that format was proper for <key>:<value>
                if len(key_value) == 2:
                    # Create/Add to search dictionary
                    search_dictionary.update({key_value[0]: key_value[1]})
                else:
                    return None
        else:
            return None
    else:
        return None
    return search_dictionary
