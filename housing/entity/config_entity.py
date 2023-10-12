from collections import namedtuple

'''
1.Dataset Download URL
2.Compressed File Folder(.zip)
3.Extracted File Folder
4.Train Dataset Folder
5.Test Dataset Folder
'''
DataIngestionConfig=namedtuple(typename='DataIngestionConfig',
                               field_names=['dataset_download_url', #Dataset Download URL
                                             'tgz_download_dir', #Compressed File Folder(.zip)
                                             'raw_data_dir', #Extracted File Folder
                                             'ingested_train_dir', #Train Dataset Folder
                                             'ingested_test_dir' #Test Dataset Folder
                                              ])

DataValidationConfig=namedtuple(typename='DataValidationConfig',
                                field_names=['schema_file_path','report_file_path','report_page_file_path'])


DataTransformationConfig=namedtuple(typename='DataTransformationConfig',
                                    field_names=['add_bedroom_per_room',  # True/False
                                                 'transformed_train_dir', # X_train_scaled
                                                 'transformed_test_dir',  # X_test_scaled
                                                 'preprocessed_object_file_path' # StandardScaler() -> object
                                                 ])

ModelTrainerConfig=namedtuple(typename='ModelTrainerConfig',
                              field_names=['trained_model_object_file_path', # LinearRegression()
                                           'base_accuracy'
                                         ])


ModelEvaluationConfig=namedtuple(typename='ModelEvaluationConfig',
                                 field_names=['model_evaluation_object_file_path',
                                 'time_stamp'])

ModelPusherConfig=namedtuple(typename='ModelPusherConfig',
                             field_names=['export_dir_path'])

TrainingPipelineConfig=namedtuple(typename='TrainingPipelineConfig',
                                  field_names=['artifact_dir'])