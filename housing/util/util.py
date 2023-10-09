from housing.exception import HousingException
import os,sys
import yaml

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