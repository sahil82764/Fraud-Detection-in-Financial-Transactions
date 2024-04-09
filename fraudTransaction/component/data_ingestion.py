from fraudTransaction.entity.config_entity import DataIngestionConfig
import os,sys
from fraudTransaction.exception import fraudTransactionException
from fraudTransaction.logger import logging
from fraudTransaction.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import shutil
import glob

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20}Data Ingestion Log Started.{'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise fraudTransactionException(e,sys) from e

    def reading_data_path(self) -> str:
        try:
            #extraction path to read dataset
            dataset_path = self.data_ingestion_config.dataset_path
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            # Get a list of all files in the source folder
            files = os.listdir(raw_data_dir)

            # Filter the list to only include CSV files
            csv_files = [file for file in files if file.endswith('.csv')]

            # Copy each CSV file from the source folder to the destination folder
            for file in csv_files:
                source_file = os.path.join(dataset_path, file)
                destination_file = os.path.join(raw_data_dir, file)
                shutil.copyfile(source_file, destination_file)

            logging.info(f"The Data has been moved from: [{dataset_path}] to: [{raw_data_dir}]")

        except Exception as e:
            raise fraudTransactionException(e,sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            csv_files = glob.glob(os.path.join(raw_data_dir, '*.csv'))

            file_name = os.listdir(raw_data_dir)[0]

            logging.info(f"Reading csv file: [{raw_data_dir}]")
            
            # Initialize an empty list to store DataFrames
            frdTrns_data = []

            # Read each CSV file into a DataFrame and append it to the list
            for csv_file in csv_files:
                df = pd.read_csv(csv_file)
                frdTrns_data.append(df)

            # Concatenate all DataFrames in the list into a single DataFrame
            final_df = pd.concat(frdTrns_data, ignore_index=True)

            
            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index, test_index in split.split(final_df):
                strat_train_set = final_df.loc[train_index]
                strat_test_set = final_df.loc[test_index]

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting training dataset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting testing dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path = train_file_path,
                test_file_path = test_file_path,
                is_ingested = True,
                message = f"Data ingestion completed successfully"
                )

            logging.info(f"Data ingestion artifact: [{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise fraudTransactionException(e,sys) from e

    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.reading_data_path()
            return self.split_data_as_train_test()
        except Exception as e:
            raise fraudTransactionException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion Log Completed{'<<'*20}\n\n")