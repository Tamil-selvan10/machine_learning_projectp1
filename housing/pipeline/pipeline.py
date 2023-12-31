from housing.logger import logging
from housing.exception import HousingException
import os,sys
from housing.config.configuration import Configuration
from housing.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation

class Pipeline():

    def __init__(self,
                 config:Configuration=Configuration())->None:
        try:
            self.config=config

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def start_data_ingestion(self,
                             data_ingestion_config:DataIngestionConfig)->DataIngestionArtifact:
        try:
            data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys) from e
        

    def start_data_validation(self,
                              data_ingestion_artifact:DataIngestionArtifact,
                              data_validation_config:DataValidationConfig)->DataValidationArtifact:
        try:
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=data_validation_config)
            
            return data_validation.initiate_data_validation()

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def start_data_transformation(self,
                                  data_transformation_config:DataTransformationConfig,
                                  data_ingestion_artifact:DataIngestionArtifact,
                                  data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:

            data_transformation=DataTransformation(data_transformation_config=data_transformation_config,
                               data_ingestion_artifact=data_ingestion_artifact,
                               data_validation_artifact=data_validation_artifact)
            
            return data_transformation.initiate_data_transformation()
        
        except Exception as e:
            raise HousingException(e,sys) from e
        

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion(data_ingestion_config=self.config.get_data_ingestion_config())
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact,
                                                                data_validation_config=self.config.get_data_validation_config())
            
            data_transformation_artifact=self.start_data_transformation(data_transformation_config=self.config.get_data_transformation_config(),
                                           data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_artifact=data_validation_artifact)
        except Exception as e:
            raise HousingException(e,sys) from e