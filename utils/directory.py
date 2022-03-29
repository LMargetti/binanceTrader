import pathlib
from pathlib import Path


class Directory:
    @staticmethod
    def get_data_dir(self, data_folder: str):

        # Collecting cwd and folder
        cwd = Path.cwd()
