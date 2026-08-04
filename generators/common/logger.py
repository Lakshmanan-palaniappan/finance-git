import logging

from generators.common.config import LOG_LEVEL

logging.basicConfig(

    level=LOG_LEVEL,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger("banking-generator")