from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_filepath:str
    train_file_path:str
    test_file_path:str