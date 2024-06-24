import logging
import sqlalchemy

logging.basicConfig()
logger = logging.getLogger('sqlalchemy')

handler = logging.FileHandler('app.log', mode="w")
handler.setLevel(logging.INFO)

logger.addHandler(handler)