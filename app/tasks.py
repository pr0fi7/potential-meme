from app.celery_app import celery
import time
import logging


logger = logging.getLogger(__name__)


@celery.task
def process_item(item_id: int):
    """Simulate streaming-processing of a newly created item.
    Avoids DB access so it works across pods without shared storage.
    """
    logger.info("Processing item_id=%s", item_id)
    time.sleep(0.1)
    logger.info("Done item_id=%s", item_id)
    return {"processed": True, "item_id": item_id}