import logging
from datetime import datetime
timestamp = datetime.now().isoformat()
log_format = '\033[34m%(asctime)s\033[0m - \033[32m%(name)s\033[0m - %(levelname)s - %(message)s'
logging.basicConfig(
    format=log_format,
    level=0,
    filename="logs/%s.log"%timestamp,
)
logging.addLevelName(logging.DEBUG, '\033[96mDebug\033[0m')
logging.addLevelName(logging.INFO, '\033[94mInfo\033[0m')
logging.addLevelName(logging.WARNING, '\033[33mWarning\033[0m')
logging.addLevelName(logging.ERROR, '\033[31mError\033[0m')
logging.addLevelName(logging.CRITICAL, '\033[41m\033[93mCritical\033[0m')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter(log_format))
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)

logger.debug("test")
logger.info("test")
logger.warning("test")
logger.error("test")
logger.critical("test")
