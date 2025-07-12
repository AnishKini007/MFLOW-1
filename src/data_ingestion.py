import os
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config['bucket_name']
        self.file_name = self.config['bucket_file_name']
        self.train_test_ratio = self.config['train_ratio']

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion started with {self.bucket_name} and {self.file_name}")

    def download_data(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"Raw data downloaded successfully from GCS: {self.file_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error downloading raw data from GCS: {e}")
            raise CustomException(f"Error downloading csv file: {e}", sys)

    def split_data(self):
        try:
            logger.info("Starting data split into train and test sets.")
            if not os.path.exists(RAW_FILE_PATH):
                raise FileNotFoundError(f"Raw data file not found at {RAW_FILE_PATH}")
            df = pd.read_csv(RAW_FILE_PATH)
            train_df, test_df = train_test_split(df, test_size=1-self.train_test_ratio, random_state=42)
            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")
            logger.info("Data split into train and test sets successfully.")
        except Exception as e:
            logger.error("Error splitting data")
            raise CustomException("Error splitting data", e)

    def run(self):

        try:
            logger.info("Starting data ingestion process.")
            self.download_data()
            self.split_data()
            logger.info("Data ingestion process completed successfully.")
        except Exception as e:
            logger.error(f"Error during data ingestion process: {str(e)}")
        
        finally:
            logger.info("Data ingestion process finished.")

if __name__ == "__main__":

    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()