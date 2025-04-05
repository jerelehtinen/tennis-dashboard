import logging

logger = logging.getLogger("streamlit-app")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s — %(levelname)s — %(message)s'))
    logger.addHandler(handler)