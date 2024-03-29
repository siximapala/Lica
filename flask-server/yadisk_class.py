import yadisk
import os
class I_yadisk:

    def __init__(self, token, client_id = "80962dc658884279a549db8f33953722", secret_id = "d94d84dd23a6472d81b77aa8d121778f"):
        self.token = token
        self.y = yadisk.YaDisk(client_id, secret_id, token)
        self.dict_files_upload = []
        self.dict_files = dict()
        
    
    def check(self):
        if self.y.check_token():
            if not self.y.is_dir("Lica"):
                self.y.mkdir("/Lica")
            return True
        else:
            return False
    
    def update_file(self, file):
        if self.check():    
            if self.y.is_file("/Lica/" + file):
                self.y.remove(str("/Lica/" + file), permanently=True)
                self.y.upload(str(file), str("/Lica/" + file))
            else:
                self.y.upload(str(file), str("/Lica/" + file))
            print("произведена выгрузка файла на диск:" + file)    
        else:
            print(error="error")        
        

    def upload_dir(self, path):
        if self.check():
            if not self.y.is_dir(path):
                self.y.mkdir(path)

    def get_files_name(self, path):
        for item in self.y.listdir(path):
            if item['type'] == 'dir':
                self.dict_files[item['name']] = {
                    "Название": item['name'],
                    "Размер": item["size"],
                    "Тип файла": item['type'],
                    "Тип документа": item['media_type'],
                    "Дата создания": item['created'],
                    "Вложенные файлы": self.get_files_name(path + "/" + item['name'])
                }  
            else:
                self.dict_files[item['name']] = {
                    "Название": item['name'],
                    "Размер": item["size"],
                    "Тип файла": item['type'],
                    "Тип документа": item['media_type'],
                    "Дата создания": item['created']
                }  
        return self.dict_files

    def download_from_disk(self, file):
        if self.check():
            self.y.download(str("/Lica/" + file), str(file)) 
            print("произведено скачивание файла:" + file)
            self.dict_files_upload.append(file)
        
    def __del__(self):
        for file in self.dict_files_upload:
            self.update_file(file)
            os.remove(file)
            print("произведено удаление файла с компьютера:" + file)
            
    def download_all_files(self):
        self.get_files_name("Lica")
        for i in self.dict_files.keys():
            self.download_from_disk(self.dict_files[i]["Название"])
        return self.dict_files_upload