import os
import logging
import utility.Log_Manager
import yaml

class Project_Module_Generator():
    
    def __init__(self, file_name=None):
        self.file_name = file_name
        self.logger = logging.getLogger("generators." + self.__class__.__name__)
        if self.file_name == None:
            self.logger.info("Initializing project module generator")
        else:
            self.file_path = os.getcwd() + "\\..\\projectModule\\" + self.file_name + ".py"
            self.logger.info("Initializing project module generator for : %s" % file_name)        
        
    def createProjectModuleFile(self, related_page_name):
        self.logger.info("Creating project module file")
        file_exists = os.path.isfile(self.file_path)
        if file_exists:
            self.logger.warn("Project Module file %s already exists.  Either append project module methods to this or create a new project module file with different name" % self.file_name)
        else:
            try:
                with open(self.file_path, 'a') as f:
                    f.write("from selenium import webdriver \n")
                    f.write("from pageObjects import %s \n" % related_page_name)
                    f.write("\n")
                    
                self.logger.info("created stub project module file %s under projectModule" % self.file_name)
            except Exception as e:
                self.logger.exception("Error creating project module file. Trace : %s" % e)
                raise
        
    def createProjectModuleMethod(self, mtd_name, args=None):
        self.logger.info("Creating project module method stubs")
        if mtd_name in open(self.file_path).read():
            self.logger.warn("Project Module Method %s already exists under pageObjects.%s. Will not create this method again." %(mtd_name, self.file_name))
        else:
            try:
                with open(self.file_path, 'a') as f:
                    if args == None:
                        f.write("def %s(driver): \n" %(mtd_name))
                    else:
                        f.write("def %s(driver,%s): \n" %(mtd_name,args))                                            
                    f.write("\t'''Write method definition here''' \n\n")
                
                self.logger.info("created project module method %s under projectModule.%s" % (mtd_name,self.file_name))
            except Exception as e:
                self.logger.exception("Error creating project module method. Trace : %s" % e)
                raise
        
    '''
        1. This method will read from yaml, and create project module file and related method stubs
    '''
    def projectModuleGenerator(self):
        self.logger.info("Creating project module generator")
        project_module_config_path = os.getcwd() + "\\..\\config\\project_module_generator_config.yaml"
        with open(project_module_config_path, 'r') as f:
            doc = yaml.load(f)
            
        for k,v in doc.iteritems():
            for newV in v.values():
                print newV
                pmg = Project_Module_Generator(newV["name"])
                pmg.createProjectModuleFile(newV["related_page"])
                for func in newV["functions"].values():
                    if func["args"] == "none":
                        pmg.createProjectModuleMethod(func["name"])
                    else:
                        pmg.createProjectModuleMethod(func["name"],args=func["args"])
                        
    
    def main(self):
        self.projectModuleGenerator()
        
pmg = Project_Module_Generator()
pmg.main()
        
# pmg = Project_Module_Generator("Yahoo_Home_Actions")
# pmg.createProjectModuleFile("Yahoo_Home_Page")
# pmg.createProjectModuleMethod("login")
# pmg.createProjectModuleMethod("logout")