import logging
import utility.Log_Manager
import os
from selenium.webdriver.common.by import By
import yaml

'''
    1. Read info from yaml file
    2. Create multiple page object files at the same time
    3. It will act like ROR migration, for the page object files created, it will only append method if there are any new
    4. If page object files not created, it will create new file and add methods
'''
class Page_Object_Generator():
    
    def __init__(self, page_name=None):
        self.page = page_name
        self.logger = logging.getLogger("generators." + self.__class__.__name__)
        if self.page == None:
            self.logger.info("Initializing page object generator")
        else:
            self.file_path = os.getcwd() + "\\..\\pageObjects\\" + self.page + "_Page.py"
            self.logger.info("Initializing page object generator for : %s" % page_name + "_Page")        
        
    def createPageObjectFile(self):
        self.logger.info("starting creation of page object file")
        file_exists = os.path.isfile(self.file_path)
        if file_exists:
            self.logger.warn("Page Object file %s already exists.  Either append page object methods to this or create a new page object file with different name" % self.file_path)
        else:
            '''
                1. Create file with <page_name>_Page.py
                2. Add the initial imports which will definitely be used irrespective. 
            '''
            try:     
                with open(self.file_path, 'a') as f:
                    f.write("from selenium.webdriver.support.wait import WebDriverWait \n")
                    f.write("from selenium import webdriver \n")
                    f.write("from selenium.webdriver.common.by import By \n")
                    f.write("from selenium.webdriver.support import expected_conditions as EC \n")
                    f.write("from selenium.common.exceptions import TimeoutException \n")
                    f.write("import logging \n")
                    f.write("import utility.Log_Manager \n\n")
                    logger_cmd = "logger = logging.getLogger('%s_Page')\n\n" % self.page
                    f.write(logger_cmd)
                    
                self.logger.info("created stub page object file %s_Page under pageObjects" % self.page)
            except Exception as e:
                self.logger.exception("Unable to create page object file %s . Trace %s" % (self.page, e))
                raise
            
    def generatePageObjectMethod(self, logical_obj_name, how, what):
        self.logger.info("starting generation of page object method")
        
        '''
            TODO: 1. Add check to verify whether the method with same logical name exists.
            2. If exists, do not create page object method again, and continue to the next method definition
            3. If does not exist, create the page object method as usual
        '''
        
        if logical_obj_name in open(self.file_path).read():
            self.logger.warn("Page Object Method %s already exists under pageObjects.%s_Page. Will not create this method again." %(logical_obj_name, self.page))
        else:
            try:
                with open(self.file_path, 'a') as f:
                    f.write("\n")
                    f.write("def %s(dr): \n" % logical_obj_name)
                    f.write("\tdr.wait = WebDriverWait(dr, 30) \n")
                    f.write("\ttry: \n")
                    if how == "name":
                        f.write("\t\telement = dr.wait.until(EC.presence_of_element_located((By.NAME, '%s'))) \n" % what)
                    f.write("\texcept TimeoutException: \n")
                    f.write("\t\tlogger.exception('%s not found.') \n" % logical_obj_name)
                    f.write("\t\traise \n")
                    f.write("\texcept Exception: \n")
                    f.write("\t\tlogger.exception('%s not found.') \n" % logical_obj_name)
                    f.write("\t\traise \n")
                    f.write("\treturn element \n")    
                self.logger.info("created page object method %s under pageObjects.%s_Page" % (logical_obj_name,self.page))
            except Exception as e:
                self.logger.exception("Unable to create page object method %s under pageObjects.%s_Page. Trace %s" % (logical_obj_name, self.page, e))
                raise
        
    def deletePageObjectMethod(self, mtd_name):
        self.logger.debug("Deleting method %s from pageObjects.%s_Page" %(mtd_name, self.page))
        
    def createPageObjectsFromConfig(self):
        self.logger.info("Beginning creation of Page Object File and its methods")
        page_obj_generator_config_path = os.getcwd() + "\\..\\config\\page_object_generator_config.yaml"
        with open(page_obj_generator_config_path, 'r') as f:
            doc = yaml.load(f)
        
        '''
            TODO: Check how to manage multiple attribute to identify element
        '''
        for k, v in doc.iteritems():
            for pg in v.keys():
                print "page name:", v[pg]["name"]
                pog = Page_Object_Generator(v[pg]["name"])
                pog.createPageObjectFile()
                
                for elem in v[pg]["elements"]:
                    how_what = v[pg]["elements"][elem]
                    how_what_split = how_what.split(",")
                    how = how_what_split[0]
                    what = how_what_split[1]
                    pog.generatePageObjectMethod(elem,how,what)
        
    def main(self):
        self.createPageObjectsFromConfig()

pg = Page_Object_Generator()
pg.main()

'''Example Test Run'''
# pog.createPageObjectFile()
# pog.generatePageObjectMethod("select_Male", "name", "male")
# pog.generatePageObjectMethod("radio_Yes", "name", "Yes")
# pog.generatePageObjectMethod("select_Male", "name", "male")
# pog.generatePageObjectMethod("textField_Search", "name", "search")
# pog.generatePageObjectMethod("link_Google", "name", "goog")