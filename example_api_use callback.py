import json
import logging
import sys
import time

from dataclasses import asdict
from datetime import datetime

from pyelitecloud import EliteCloudApi, EliteCloudApiFlag, EliteCloudSite

# Setup logging to StdOut
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


TEST_USERNAME = "fill in your SmartWater username here"
TEST_PASSWORD = "fill in your SmartWater password here"
#
# Comment out the line below if username and password are set above
from tests import TEST_USERNAME, TEST_PASSWORD


def main():
    api = None
    try:
        # Process these calls in the right order
        flags = {
            EliteCloudApiFlag.RENEW_HANDLER_START: True,
        }        
        api = EliteCloudApi(TEST_USERNAME, TEST_PASSWORD, flags=flags)

        # Retrieve sites available to this user.
        sites = api.fetch_sites()

        for site in sites:
            site_uuid = site.get('uuid')
            site_name = site.get('name')

            logger.info("")
            logger.info(f"site '{site_name}':")
            logger.info(json.dumps(site, indent=4))

            site_resources = api.fetch_site_resources(site_uuid)

            logger.info("")
            logger.info(f"site '{site_name}' resources:")
            logger.info(json.dumps(site_resources, indent=4))

        # Once the sites and their resources are available, subscribe to update events
        # This will return the initial value and any changes.
        for site in sites:
            site_uuid = site.get('uuid')

            api.subscribe_site_status(site_uuid, on_site_status)

        # Keep the application alive
        for t in range(500):
            logger.info("")
            logger.info(f"wait")
            time.sleep(300)

    except Exception as e:
        logger.info(f"Unexpected exception: {e}")

    finally:
        if api:
            api.close()


def on_site_status(site: EliteCloudSite, status: dict):
    logger.info("")
    logger.info(f"site '{site.name}' status:")
    logger.info(json.dumps(status, indent=4))


# main loop
main()