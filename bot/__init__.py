import logging
from datetime import datetime
timestamp = datetime.now().isoformat()
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=log_format,
    level=0,
    filename="logs/%s.log"%timestamp,
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter(log_format))
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)

logger.debug("start")
logger.info("start")
logger.warning("start")
