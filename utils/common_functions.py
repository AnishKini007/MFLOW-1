import os
import pandas
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML file not found at {file_path}")
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"YAML file read successfully from {file_path}")
            return config
    except Exception as e:
        logger.error(f"Error reading YAML file at {file_path}: {e}")
        raise CustomException(f"Error reading YAML file at {file_path}: {e}")

def load_data(path):
    try:
        logger.info(f"Loading data from {path}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Data file not found at {path}")
        df = pandas.read_csv(path)
        logger.info(f"Data loaded successfully from {path}")
        return df
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        raise CustomException(f"Error loading data from {path}: {e}")

