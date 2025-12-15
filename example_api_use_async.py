import asyncio
import json
import logging
import sys

from dataclasses import asdict
from datetime import datetime

from pyelitecloud import AsyncEliteCloudApi

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


async def main():
    api = None
    try:
        # Process these calls in the right order
        api = AsyncEliteCloudApi(TEST_USERNAME, TEST_PASSWORD)

        # Retrieve sites available to this user.
        sites = await api.fetch_sites()

        for site in sites:
            site_uuid = site.get('uuid')
            site_name = site.get('name')

            logger.info("")
            logger.info(f"site '{site_name}':")
            logger.info(json.dumps(site, indent=4))

            site_resources = await api.fetch_site_resources(site_uuid)

            logger.info("")
            logger.info(f"site '{site_name}' resources:")
            logger.info(json.dumps(site_resources, indent=4))

        # Once the sites and their resources are available, the calls below can be repeated periodically.
        for t in range(30):
            # Retrieve gateway(s) for the profile
            for site in sites:
                site_uuid = site.get('uuid')
                site_name = site.get('name')
                site_status = await api.fetch_site_status(site_uuid)

                logger.info("")
                logger.info(f"site '{site_name}' status:")
                logger.info(json.dumps(site_status, indent=4))

            # Wait a couple of minutes and retrieve statuses again
            logger.info("")
            logger.info(f"wait")
            await asyncio.sleep(300)

    except Exception as e:
        logger.info(f"Unexpected exception: {e}")

    finally:
        if api:
            await api.close()


# main loop
asyncio.run(main()) 