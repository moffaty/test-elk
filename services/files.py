import json
import os

class FileSystem:
    @staticmethod
    def parse_json(path: str):         
        with open(path, 'r', encoding='utf-8') as file:
            file_data = json.load(file)
        return file_data
    
    @staticmethod
    def create_doc(index_name: str, data: dict[str, str]):
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
                    print(f"Ошибка при удалении файла {file_path}: {e}")
            
            try:
                os.rmdir(directory_path)
            except Exception as e:
                print(f"Ошибка при удалении директории {directory_path}: {e}")