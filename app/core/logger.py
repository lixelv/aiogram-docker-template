import logfire
import logging

from .config import LOGFIRE_TOKEN


def setup_logging():
    logfire.configure(send_to_logfire=bool(LOGFIRE_TOKEN))

    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.basicConfig(handlers=[logfire.LogfireLoggingHandler()])

    logfire.info("Logging is complained!")
