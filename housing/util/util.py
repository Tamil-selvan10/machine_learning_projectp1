from housing.exception import HousingException
import os,sys
import yaml
import numpy as np
import pandas as pd
from housing.constant import *
import dill


def read_yaml_file(file_path:str)->dict:
    '''
    Reads a YAML file and return the contents as a dictionary.
    file_path:str
    '''
    try:
        with open(file=file_path,mode='rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e
    

def load_data(file_path:str,schema_file_path:str)->pd.DataFrame:
    try:
        dataset_schema=read_yaml_file(file_path=schema_file_path)
        schema=dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]
        
        dataframe=pd.read_csv(file_path)

        error_message=None

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message=f'column:{column} is not in the schema'

        if error_message is not None:
            raise Exception(error_message)
        
        return dataframe
    
    except Exception as e:
        raise HousingException(e,sys) from e
    

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file=file_path,mode='wb') as file_obj:
            np.save(file_obj,array)

    except Exception as e:
        raise HousingException(e,sys) from e
    

def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file=file_path,mode='rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def save_object(file_path:str,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file=file_path,mode='wb') as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise HousingException(e,sys) from e
    
def load_object(file_path:str):
    try:
        with open(file=file_path,mode='rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e