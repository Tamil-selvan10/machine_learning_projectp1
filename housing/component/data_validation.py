from typing import Any
from housing.logger import logging
from housing.exception import HousingException
import os,sys
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import numpy as np
import pandas as pd
#from evidently.model_profile import Profile
#from evidently.model_profile.sections import DataDriftProfileSection

#from evidently.dashboard import Dashboard
#from evidently.dashboard.tabs import DataDriftTab
import json



class DataValidation():

    def __init__(self,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig)-> None:
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20}")
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
        except Exception as e:
            raise HousingException(e,sys) from e

    #1.Train and test File exists?
    def is_train_and_test_file_exist(self):
        try:

            is_train_file_exist=False
            is_test_file_exist=False

            is_train_file_exist=os.path.exists(self.data_ingestion_artifact.train_file_path)
            is_test_file_exist=os.path.exists(self.data_ingestion_artifact.test_file_path)

            is_available=is_train_file_exist and is_test_file_exist

            if not is_available:
                train_file_path=self.data_ingestion_artifact.train_file_path
                test_file_path=self.data_ingestion_artifact.test_file_path
                message=f'Train File [{train_file_path}] or Test File [{test_file_path}] is not present'
                raise Exception(message)

        except Exception as e:
            raise HousingException(e,sys) from e 

    #2.Validate dataset schema
    def validate_dataset_schema(self):
        try:
            
            validation_status=True

            #1.File name:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            train_file_name=os.path.basename(train_file_path)
            test_file_name=os.path.basename(test_file_path)

            if train_file_name!=test_file_name:
                validation_status=False


            #2.Number of Columns:
            train_data=pd.read_csv(train_file_path)
            test_data=pd.read_csv(test_file_path)

            total_train_col=len(train_data.columns.to_list())
            total_test_col=len(test_data.columns.to_list())

            if total_train_col!=total_test_col:
                validation_status=False


            #3.Name of Columns:
            train_col_names=sorted(train_data.columns.to_list(),reverse=False)
            test_col_names=sorted(test_data.columns.to_list(),reverse=False)

            if train_col_names!=test_col_names:
                validation_status=False

            return validation_status

        except Exception as e:
            raise HousingException(e,sys) from e  
        
    def get_train_and_test_df(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            return train_df,test_df

        except Exception as e:
            raise HousingException(e,sys) from e
        
    '''
    def save_data_drift_report(self):
        try:
            profile=Profile(sections=[DataDriftProfileSection()])
            train_df,test_df=self.get_train_and_test_df()
            profile.calculate(train_df,test_df)

            report=json.loads(profile.json())

            report_file_path=self.data_validation_config.report_file_path
            report_dir=os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(file=report_file_path,mode='w') as report_file:
                json.dump(report,report_file,indent=6)

        except Exception as e:
            raise HousingException(e,sys) from 
    
    def save_data_drift_report_page(self):
        try:
            dashboard=Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path=self.data_validation_config.report_page_file_path
            report_page_dir=os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)


        except Exception as e:
            raise HousingException(e,sys) from e
    '''


    #3. is data drift found?
    def is_data_drift_found(self):
        try:
           # self.save_data_drift_report()
           # self.save_data_drift_report_page()
           pass

        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_and_test_file_exist()
            self.validate_dataset_schema()
            self.is_data_drift_found()
            data_validation_artifact=DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path, 
                                   report_file_path=self.data_validation_config.report_file_path, 
                                   report_page_file_path=self.data_validation_config.report_page_file_path, 
                                   is_validated=True, 
                                   message='Data Validation Completed Successfully')
            logging.info(f'Data Validation Artifact:{data_validation_artifact}')
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        

    def __del__(self):
        logging.info(f"{'='*20}Data Validation log completed.{'='*20}")