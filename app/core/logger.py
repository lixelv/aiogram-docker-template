import logfire
import logging


def setup_logging():
    logfire.configure(send_to_logfire=False)

    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.basicConfig(handlers=[logfire.LogfireLoggingHandler()])

    logfire.info("Logging is complained!")
