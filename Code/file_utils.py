import os
import shutil
from datetime import datetime

class FileManager:
    TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")

    @staticmethod
    def create_folders(folders):
        for i in range(len(folders)):
            folders[i] = os.path.join(folders[i], FileManager.TIMESTAMP)
            os.makedirs(folders[i], exist_ok=True)
        return folders

    @staticmethod
    def move_files_to_folders(files, folder_mapping):
        for file in files:
            for extension, base_folder in folder_mapping.items():
                if file.endswith(extension):
                    target_folder = os.path.join(base_folder, FileManager.TIMESTAMP)
                    shutil.move(file, os.path.join(target_folder, file))