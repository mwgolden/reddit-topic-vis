import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):

    logger.info("## Event Object ##")
    logger.info(event)

    
    return {
        "statusCode": 200,
        "body": ""
    }