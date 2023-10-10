from housing.logger import logging
from housing.exception import HousingException
import os,sys
from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from six.moves import urllib
import tarfile
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion():

    def __init__(self,
                 data_ingestion_config:DataIngestionConfig)->None:
        try:
            logging.info(f"{'='*20}Data Ingestion Log Started.{'='*20}")
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise HousingException(e,sys) from e
        

    def download_housing_data(self)->str:
        try:
            #Remote URL to download dataset
            dataset_download_url=self.data_ingestion_config.dataset_download_url

            #.tgz file folder/dir
            tgz_download_dir=self.data_ingestion_config.tgz_download_dir

            os.makedirs(tgz_download_dir,exist_ok=True) 

            #filename(housing.tgz)
            filename=os.path.basename(dataset_download_url)

            #.tgz file path
            tgz_file_path=os.path.join(tgz_download_dir,filename)
            
            logging.info(f'Downloading file from:[{dataset_download_url}] into dir:[{tgz_file_path}]')
            
            urllib.request.urlretrieve(url=dataset_download_url,filename=tgz_file_path)
            
            logging.info('Dataset Downloaded successfully')

            return tgz_file_path

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def extract_tgz_file(self,tgz_file_path:str)->None:
        try:
        
            raw_data_dir=self.data_ingestion_config.raw_data_dir 

            os.makedirs(raw_data_dir,exist_ok=True)
           
            logging.info(f'Extract File from:[{tgz_file_path}] into dir:[{raw_data_dir}]')
            obj=tarfile.open(name=tgz_file_path,mode='r')
            obj.extractall(path=raw_data_dir)
            logging.info('Extraction Completed Successfully')
        

        except Exception as e:
            raise HousingException(e,sys) from e
        
    
    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            #raw_data_dir
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            #filename(housing.csv)
            filename=os.listdir(raw_data_dir)[0]

            #raw data file path
            raw_data_file_path=os.path.join(raw_data_dir,filename)

            #train file path
            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,filename)

            #test file path
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,filename)
            
            logging.info(f'Reading .csv file from :[{raw_data_file_path}]')
            housing_data_frame=pd.read_csv(raw_data_file_path)
            housing_data_frame['income_cat']=pd.cut(housing_data_frame['median_income'],
                                                    bins=[0.0,1.5,3.0,4.5,6.0,np.inf],
                                                    labels=[1,2,3,4,5])
            
            logging.info('Split dataset into Train and Test')

            strat_train_set=None
            strat_test_set=None

            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)


            for train_index,test_index in split.split(housing_data_frame,housing_data_frame['income_cat']):
                strat_train_set=housing_data_frame.loc[train_index].drop(columns=['income_cat'],axis=1)
                strat_test_set=housing_data_frame.loc[test_index].drop(columns=['income_cat'],axis=1)
            
            logging.info(f'Exporting train data into file path:[{train_file_path}]')
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                strat_train_set.to_csv(train_file_path,index=False)

            logging.info(f'Exporting test data into file path:[{test_file_path}]')

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                strat_test_set.to_csv(test_file_path,index=False)
            
            data_ingestion_artifact=DataIngestionArtifact(train_file_path=train_file_path, 
                                  test_file_path=test_file_path, 
                                  is_ingested=True, 
                                  message='Data Ingestion Completed Successfully')
            
            logging.info(f'Data ingestion artifact:{data_ingestion_artifact}')

            return data_ingestion_artifact
        
        except Exception as e:
            raise HousingException(e,sys) from e
        
    
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path=self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(e,sys) from e
        

    def __del__(self):
        logging.info(f"{'='*20} Data Ingestion Log Completed.{'='*20}")
                  
                
