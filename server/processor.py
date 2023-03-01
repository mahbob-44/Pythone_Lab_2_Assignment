import glob
import shutil
import os
import zipfile
import subprocess

class server:
    def __init__(self,source_path,server_path,destination_path,postfixes):
        self.server_path=server_path
        self.destination_path=destination_path
        self.source_path=source_path
        self.source_objects=None
        self.postfixes=postfixes
        self.object_paths_in_server=[]
        self.modified_objects_in_server=[]
        self.processed_objects=None
    
    def capture_object_paths_from_source(self):
        self.source_objects=glob.glob(self.source_path)

    def copy_objects_to_server(self):
        for object_path in self.source_objects:
            if '.txt'in object_path:
                shutil.copy(object_path,'.')
            elif '.py' in object_path:
                result=subprocess.Popen(['python',object_path],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, errors = result.communicate()
                print(output.decode())
                print(errors.decode())
        self.object_paths=glob.glob(self.server_path)
        
    def rename_file(self):
        modified_object_name=[]
        for object_path in self.object_paths:
            object_name=object_path.split('/')[-1].split('\\')[-1].split('.')
            if object_name[1]=='txt':
                prefix=object_name[0]
                for postfix in self.postfixes:
                    modified_object_name.append(prefix + "_" +str(postfix)+'.'+object_name[1])


        return modified_object_name
    
    def write_inside_the_new_files(self):
        for object_path in self.object_paths:
            if '.txt' in object_path:
                j=0
                for postfix in self.postfixes:
                    with open (object_path,'r') as file_1:
                        lines=file_1.readlines()
                        with open(self.modified_objects_in_server[j],'w') as file_2:
                            for i in range(postfix*10):
                                file_2.write(lines[i])
                            j+=1

    def process_files(self):
        modified_object_names=self.rename_file()
        for object_path in self.object_paths:
            self.object_paths_in_server.append(object_path)
            if '.txt' in object_path:
                for modified_name in modified_object_names:
                    objects_path_in_server=f"../server/{modified_name}"
                    self.object_paths_in_server.append(objects_path_in_server)
                    self.modified_objects_in_server.append(objects_path_in_server)
                    shutil.copy(object_path,objects_path_in_server)
        self.write_inside_the_new_files()
        self.create_zip_file("temp_zip_file.zip",self.modified_objects_in_server)

    def create_zip_file(self,file_name,modified_object_names):
        with zipfile.ZipFile(file_name,"w", zipfile.ZIP_DEFLATED) as zip:
            for objects_path_in_server in modified_object_names:
                zip.write(objects_path_in_server)
        for object_path in self.object_paths_in_server:
            if '.txt' in object_path:
                os.remove(object_path)
        self.capture_object_file_from_server()
    def capture_object_file_from_server(self):
        self.processed_objects=glob.glob(self.server_path)
        for processed in self.processed_objects:
            if '.zip' in processed:
               processed_name=self.destination_path+'\\'+processed.split('\\')[-1]
            
               shutil.copy(processed,processed_name)
               os.remove(processed)
    def unzip_the_processed_objects(self):
        processed_zip=glob.glob("../destination/*")
        
        with zipfile.ZipFile(processed_zip[0],"r") as zip:
            zip.extractall("D:\phitron.io\Python_Lab_2 of course _4\destination")
                
    # def send_zip_file_to_destination(self):

        


source_path='../source/*'
server_path='../server/*'
destination_path='../destination'

server_1=server(source_path,server_path,destination_path,[1,2,3])
server_1.capture_object_paths_from_source()
server_1.copy_objects_to_server()
server_1.process_files()
server_1.unzip_the_processed_objects()
