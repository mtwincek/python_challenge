import argparse
import os
import logging
import sys
import src.IPAddressProcessor as IPAddressProcessor
log = logging.getLogger(__name__)


def main():
    # Set basic logging
    logging.basicConfig(stream=sys.stdout,
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # Checked passed parameters
    parser = argparse.ArgumentParser(description="Parse and query file of IP addresses.")
    parser.add_argument("-f", "--file", help="file to parse for IP addresses", required=True)
    parser.add_argument("--debug", help="turn on debug mode", action="store_true", required=False)
    args = parser.parse_args()

    # Set all input variables
    file_input = str(args.file)
    debug_input = args.debug

    # Check for debug mode
    if debug_input:
        logging.getLogger().setLevel(level="DEBUG")
        log.debug("Logging level set to \"DEBUG\"")

    # Validate input file exists
    if not os.path.isfile(file_input):
        log.error("File \"%s\" does not exist" % file_input)
        raise SystemExit

    # Run IP Address Processor
    try:
        IPAddressProcessor.ip_address_processor(file_input)
    except Exception as exc_err:
        log.exception(str(exc_err))
        raise SystemExit

if __name__ == "__main__":
    main()
