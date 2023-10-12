from housing.logger import logging
from housing.exception import HousingException
import os,sys
from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.compose import ColumnTransformer
from housing.constant import *
import numpy as np
import pandas as pd
from housing.util.util import *
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder


class FeatureGenerator(BaseEstimator,TransformerMixin):
    def __init__(self,
                 add_bedroom_per_room:bool=True,
                 total_rooms_ix:int=3,
                 total_bedrooms_ix:int=4,
                 population_ix:int=5,
                 households_ix:int=6,
                 columns=None
                 ):
        try:
            self.columns=columns
            if self.columns is not None:
                total_rooms_ix=self.columns.index(COLUMN_TOTAL_ROOMS)
                total_bedrooms_ix=self.columns.index(COLUMN_TOTAL_BEDROOM)
                population_ix=self.columns.index(COLUMN_POPULATION)
                households_ix=self.columns.index(COLUMN_HOUSEHOLDS)

            self.add_bedroom_per_room=add_bedroom_per_room
            self.total_rooms_ix=total_rooms_ix
            self.total_bedrooms_ix=total_bedrooms_ix
            self.population_ix=population_ix
            self.households_ix=households_ix

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def fit(self,X,y=None):
        return self
    
    def transform(self,X,y=None):
        try:
            room_per_household=X[:,self.total_rooms_ix]/ \
                               X[:,self.households_ix]
            
            population_per_household=X[:,self.population_ix]/ \
                                     X[:,self.households_ix]
            
            error_message = None

            if self.add_bedroom_per_room:
                bedroom_per_room=X[:,self.total_bedrooms_ix]/ \
                                 X[:,self.total_rooms_ix]
                
                generated_feature=np.c_[room_per_household,population_per_household,bedroom_per_room]
            
            else:
                generated_feature=np.c_[room_per_household,population_per_household]

            return generated_feature

        except Exception as e:
            raise HousingException(e,sys) from e

        





class DataTransformation():

    def __init__(self,
                 data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact)-> None:
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
  
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_data_transformer_object(self)-> ColumnTransformer:
        try:

            schema_file_path=self.data_validation_artifact.schema_file_path

            dataset_schema=read_yaml_file(file_path=schema_file_path)

            numerical_columns=dataset_schema[NUMERICAL_COLUMNS_KEY]
            categorical_columns=dataset_schema[CATEGORICAL_COLUMNS_KEY]

            num_pipeline=Pipeline(steps=[
                        ('imputer',SimpleImputer(strategy='median')),
                        ('feature_generator',FeatureGenerator(
                            add_bedroom_per_room=self.data_transformation_config.add_bedroom_per_room,
                            columns=numerical_columns)),
                        ('scaler',StandardScaler())])
            
            cat_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder',OneHotEncoder())])
            

            preprocessing_obj=ColumnTransformer(transformers=[
                ('num_pipeline',num_pipeline,numerical_columns),
                ('cat_pipeline',cat_pipeline,categorical_columns)
            ])

            return preprocessing_obj

        except Exception as e:
            raise HousingException(e,sys) from e
        

    def initiate_data_transformation(self)->DataTransformationArtifact:

        try:

            #preprocessed obj
            preprocessing_obj=self.get_data_transformer_object()

            #schema file path
            schema_file_path=self.data_validation_artifact.schema_file_path

            #obtain train and test file path
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #obtain train and test dataframe
            train_df=load_data(file_path=train_file_path,schema_file_path=schema_file_path)
            test_df=load_data(file_path=test_file_path,schema_file_path=schema_file_path)

            #obtain target column name
            dataset_schema=read_yaml_file(file_path=self.data_validation_artifact.schema_file_path)
            target_column_name=dataset_schema[TARGET_COLUMNS_KEY]

            #obtain train and test data
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            output_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            output_feature_test_df=test_df[target_column_name]


            #Transform Train and Test data
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr=np.c_[input_feature_train_arr,np.array(output_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(output_feature_test_df)]

            #obtain train and test file name
            train_file_name=os.path.basename(train_file_path).replace('.csv','.npz')
            test_file_name=os.path.basename(test_file_path).replace('.csv','.npz')

            transformed_train_dir=self.data_transformation_config.transformed_train_dir
            transformed_test_dir=self.data_transformation_config.transformed_test_dir

            transformed_train_file_path=os.path.join(transformed_train_dir,
                                                     train_file_name)
            
            transformed_test_file_path=os.path.join(transformed_test_dir,
                                                    test_file_name)
            
            preprocessed_object_file_path=self.data_transformation_config.preprocessed_object_file_path

            # Saving Train and Test numpy array data
            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            # Saving Preprocessed Obj
            save_object(file_path=preprocessed_object_file_path,obj=preprocessing_obj)

            data_transformation_artifact=DataTransformationArtifact(transformed_train_file_path=transformed_train_file_path, 
                                       transformed_test_file_path=transformed_test_file_path, 
                                       preprocessed_object_file_path=preprocessed_object_file_path, 
                                       is_transformed=True, 
                                       message='Data Transformation Completed Successfully')
            
            logging.info(f'Data Transformation Artifact:{data_transformation_artifact}')

            return data_transformation_artifact


        except Exception as e:
            raise HousingException(e,sys) from e
        

    def __del__(self):
        logging.info(f"{'='*20}Data Transformation log completed.{'='*20}")