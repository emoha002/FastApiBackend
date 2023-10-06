import logging
import os

# Ensure the directory exists
os.makedirs('logs', exist_ok=True)

def log_creator(logger_name: str) -> logging.Logger:

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create a loger handler
    # FIXME change the w to a during deployement

    handler = logging.FileHandler(f'logs/{logger_name}.log', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger


fast_api_logger = log_creator('fastapi')
sqlalchemy_logger = log_creator('sqlalchemy')
