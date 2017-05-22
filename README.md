# python_challenge
This project is written in Python3

This program will
1) Take a text file as input
2) Find all IP addresses in the text
3) Call APIs GeoIP and RDAP then store returned information
4) Allow user to search IP address information collected via query commands described while running the program

For help run:

    ip_lookup.py --help

HELP OUTPUT:

    usage: ip_lookup.py [-h] -f FILE [--debug]

    optional arguments:

      -h, --help            show this help message and exit

      -f FILE, --file FILE  file to parse for IP addresses

      --debug               turn on debug mode

To run program:

    python ip_lookup.py --file data/list_of_ips.txt
