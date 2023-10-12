from collections import namedtuple

DataIngestionArtifact=namedtuple(typename='DataIngestionArtifact',
                                 field_names=['train_file_path',
                                              'test_file_path',
                                              'is_ingested',
                                              'message'])

DataValidationArtifact=namedtuple(typename='DataValidationArtifact',
                                  field_names=['schema_file_path',
                                               'report_file_path',
                                               'report_page_file_path',
                                               'is_validated',
                                               'message'])

DataTransformationArtifact=namedtuple(typename='DataTransformationArtifact',
                                      field_names=['transformed_train_file_path',
                                                   'transformed_test_file_path',
                                                   'preprocessed_object_file_path',
                                                   'is_transformed',
                                                   'message'])