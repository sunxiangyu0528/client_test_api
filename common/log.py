import logging
import os
from logging.handlers import RotatingFileHandler
LOG_SIZE = 1 * 1024 * 1024

base = os.path.dirname(os.path.dirname(__file__))
df = base + "/logs/ltp_debug.log"
ef = base + "/logs/ltp_error.log"

logger = logging.getLogger("ltp")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s - %(levelname)s]:  %(message)s")


debug = RotatingFileHandler(df, maxBytes=LOG_SIZE, backupCount=1)
debug.setLevel(logging.DEBUG)
debug.setFormatter(formatter)

error = logging.FileHandler(ef)
error.setLevel(logging.ERROR)
error.setFormatter(formatter)

logger.addHandler(debug)
logger.addHandler(error)

