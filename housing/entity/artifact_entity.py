from collections import namedtuple

DataIngestionArtifact=namedtuple(typename='DataIngestionArtifact',
                                 field_names=['train_file_path',
                                              'test_file_path',
                                              'is_ingested',
                                              'message'])