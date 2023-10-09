from housing.constant import *
from housing.exception import HousingException
import os,sys
from housing.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig\
,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig,TrainingPipelineConfig
from housing.util.util import read_yaml_file
from housing.logger import logging

class Configuration():

    def __init__(self,
                 config_file_path:str=CONFIG_FILE_PATH,
                 current_time_stamp:str=CURRENT_TIMESTAMP) -> None:
        
        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.time_stamp=current_time_stamp
            self.training_pipeline_config=self.get_training_pipeline_config()
            self.data_ingestion_config=self.get_data_ingestion_config()

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            data_ingestion_info=self.config_info[DATA_INGESTION_CONFIG_KEY]
            
            dataset_download_url=data_ingestion_info[DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY]
             
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(artifact_dir,
                                                     DATA_INGESTION_ARTIFACT_DIR_KEY,
                                                     self.time_stamp)
            tgz_download_dir=os.path.join(data_ingestion_artifact_dir,
                                          data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY])

            raw_data_dir=os.path.join(data_ingestion_artifact_dir,
                                      data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])
            
            ingested_dir=data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]

            ingested_train_dir=os.path.join(data_ingestion_artifact_dir,
                                            ingested_dir,
                                            data_ingestion_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY])
            ingested_test_dir=os.path.join(data_ingestion_artifact_dir,
                                           ingested_dir,
                                           data_ingestion_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY])

            data_ingestion_config=DataIngestionConfig(dataset_download_url=dataset_download_url, # 1.Dataset Download URL
                                                      tgz_download_dir=tgz_download_dir,         # 2.Compressed File Folder(.zip)                
                                                      raw_data_dir=raw_data_dir,                 # 3.Extracted File Folder
                                                      ingested_train_dir=ingested_train_dir,     # 4.Train Dataset folder
                                                      ingested_test_dir=ingested_test_dir)       # 5.Test Dataset Folder
            logging.info(f'Data Ingestion Config:{data_ingestion_config}')

            return data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        pass

    def get_data_transformation_config(self)->DataTransformationConfig:
        pass

    def get_model_trainer_config(self)->ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self)->ModelPusherConfig:
        pass

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_info=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            pipeline_name=training_pipeline_info[TRAINING_PIPELINE_NAME_KEY]
            artifact_dir=os.path.join(ROOT_DIR,
                                      pipeline_name,
                                      training_pipeline_info[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f'Training Pipeline Config:{training_pipeline_config}')
            
            return training_pipeline_config

        except Exception as e:
            raise HousingException(e,sys) from e