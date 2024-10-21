import json
import os

class FileSystem:
    @staticmethod
    def get_dir(path: str):
        data = []
        
        if not os.path.isdir(path):
            raise FileNotFoundError(f"The directory {path} does not exist.")
        
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path) and filename.endswith('.json'):
                try:
                    file_data = FileSystem.parse_json(file_path)
                    data.append(file_data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {file_path}")
                except Exception as e:
                    print(f"An error occurred while reading {file_path}: {e}")
        
        return data

    @staticmethod
    def parse_json(path: str):    
        with open(path, 'r', encoding='utf-8') as file:
            file_data = json.load(file)
        return file_data
    
    @staticmethod
    def create_doc(index_name: str, data: dict[str, str]):
        os.makedirs(index_name, exist_ok=True)
        file_name = f"{index_name}/{data['id']}.json" 
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def delete_docs(index_name: str) -> None:
        directory_path = os.path.join(index_name)
        
        if os.path.exists(directory_path):
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Error in deleting file {file_path}: {e}")
            
            try:
                os.rmdir(directory_path)
            except Exception as e:
                print(f"Error in deleting dir {directory_path}: {e}")