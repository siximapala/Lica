import yadisk
import os
class I_yadisk:

    def __init__(self, token, client_id = "80962dc658884279a549db8f33953722", secret_id = "d94d84dd23a6472d81b77aa8d121778f"):
        self.token = token
        self.y = yadisk.YaDisk(client_id, secret_id, token)
        self.dict_files_upload = []
        
    
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
        else:
            print(error="error")        
        

    def upload_dir(self, path):
        if self.check():
            if not self.y.is_dir(path):
                self.y.mkdir(path)

    def get_files_name(self, path):
        dict_files = dict()
        for item in self.y.listdir(path):
            if item['type'] == 'dir':
                dict_files[item['name']] = {
                    "Название": item['name'],
                    "Размер": item["size"],
                    "Тип файла": item['type'],
                    "Тип документа": item['media_type'],
                    "Дата создания": item['created'],
                    "Вложенные файлы": self.get_files_name(path + "/" + item['name'])
                }  
            else:
                dict_files[item['name']] = {
                    "Название": item['name'],
                    "Размер": item["size"],
                    "Тип файла": item['type'],
                    "Тип документа": item['media_type'],
                    "Дата создания": item['created']
                }  
        return dict_files

    def download_from_disk(self, file):
        if self.check():
            self.y.download(str("/Lica/" + file), str(file)) 
            print("произведена установка файла:" + file)
            self.dict_files_upload.append(file)
        
    def __del__(self):
        for file in self.dict_files_upload:
            self.update_file(file)
            print(self.dict_files_upload)
            os.remove(file)
        # with open("cashe_nameworkfiles.txt") as file:
        #     for i in self.dict_files_upload:
        #         file.write(i)  


# y = yadisk.YaDisk("80962dc658884279a549db8f33953722", "d94d84dd23a6472d81b77aa8d121778f", "y0_AgAAAABF_QebAAr1PwAAAAD0J7_iFf1mi2K1TICY7B-19b5bS3gXuzE")
# y.update('test.txt', '/test.txt')
# y.check

f = I_yadisk("y0_AgAAAABF_QebAAr1PwAAAAD0J7_iFf1mi2K1TICY7B-19b5bS3gXuzE")

r = f.get_files_name("Lica")
print(r)
f.update_file("test.txt")
f.download_from_disk("test.txt")
del f