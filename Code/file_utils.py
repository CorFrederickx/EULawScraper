import os
import shutil

class FileManager:
    @staticmethod
    def create_folders(folders):
        for folder in folders:
            os.makedirs(folder, exist_ok=True)

    @staticmethod
    def move_files_to_folders(files, folder_mapping):
        for file in files:
            for extension, folder in folder_mapping.items():
                if file.endswith(extension):
                    shutil.move(file, os.path.join(folder, file))
