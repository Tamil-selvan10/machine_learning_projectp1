from collections import namedtuple

DataIngestionArtifact=namedtuple(typename='DataIngestionArtifact',
                                 field_names=['train_file_path',
                                              'test_file_path',
                                              'is_ingested',
                                              'message'])

DataValidationArtifact=namedtuple(typename='DataValidationArtifact',
                                  field_names=['schema_file_path',
                                               'train_file_path',
                                               'test_file_path',
                                               'is_validated',
                                               'message'])