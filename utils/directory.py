from pathlib import Path


class Directory:
    @staticmethod
    def get_data_dir(file_name: str = None, parent_num: int = None) -> Path:
        """
        If a file name is given, then the file directory is returned.
        If not, then the cryptodata folder directory is returned.
        The directory is found with pathlib and checking if the folder/file exists.
        @param parent_num: Number of which generation of parent generation
        @param file_name: string
        @return: Path
        """

        if file_name is None:
            if parent_num is None:
                return Path.cwd() / "cryptodata"
            else:
                return Path.cwd().parents[parent_num] / "cryptodata"
        else:
            if parent_num is None:
                return Path.cwd() / "cryptodata" / file_name
            else:
                return Path.cwd().parents[parent_num] / "cryptodata" / file_name
