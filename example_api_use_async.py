import asyncio
import json
import logging
import sys
import time

from dataclasses import asdict
from datetime import datetime

from pyelitecloud import AsyncEliteCloudApi, EliteCloudApiFlag, EliteCloudSite

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
        flags = {
            EliteCloudApiFlag.RENEW_HANDLER_START: True,
            EliteCloudApiFlag.DIAGNOSTICS_COLLECT: True,
        }        
        api = AsyncEliteCloudApi(TEST_USERNAME, TEST_PASSWORD, flags=flags)

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

        # Once the sites and their resources are available, subscribe to update events
        # This will return the initial value and any changes.
        for site in sites:
            site_uuid = site.get('uuid')

            await api.subscribe_site_status(site_uuid, on_site_status)

        # Keep the application alive
        for t in range(500):
            logger.info("")
            logger.info(f"wait")
            await asyncio.sleep(300)

    except Exception as e:
        logger.info(f"Unexpected exception: {e}")

    finally:
        if api:
            await api.close()


async def on_site_status(site: EliteCloudSite, section:str, id:str, status: dict):
    """
    Can be called with either:
      site   section   id          status
    - site   "status"  None        dict containing all areas, inputs and outputs
    - site   "area"    area no.    string containing area status
    - site   "output"  output no.  string containing output status
    - site   "input"   input no.   array containing input statuses
    """
    if section == "status":
        # Already logged as debug in caller
        logger.info("")
        logger.info(f"site '{site.name}' {section}:")
        logger.info(json.dumps(status, indent=4))
        pass
    else:
        # Already logged as debug in caller
        logger.info("")
        logger.info(f"site '{site.name}' {section} {id}:")
        logger.info(json.dumps(status))
        pass


# main loop
asyncio.run(main())  # main loop