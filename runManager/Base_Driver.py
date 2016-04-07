# from unittest import TestLoader, TextTestRunner, TestSuite
import unittest
import os
import testScripts
import time
from ConfigParser import SafeConfigParser
from utility.HTMLTestRunner import HTMLTestRunner
# from testScripts.SuiteC.google_search import Google_Search

#Sample example to run programmatically
# if __name__ == "__main__":
# 
#     loader = TestLoader()
#     suite = TestSuite((
#         loader.loadTestsFromTestCase(Google_Search)
#         ))
# 
#     runner = TextTestRunner(verbosity = 2)
#     runner.run(suite)


class Base_Driver():
    
#     def importAllTestScriptModules(self):
#         print "beginning to import all modules in testScripts"
        #1. Iterate through all subfolders in testScripts
        #2. For each subfolder, iterate through all .py files
        #3. Import all modules    
     
#     def addTestsToSuite(self, test_name):
#         print "adding tests to suite..."
#         suite = unittest.TestSuite()
#         suite.addTest(unittest.makeSuite(test_name))
#         return suite
     
    #TODO: Form an xml file with the list
    # of test cases that need to be run as part of a suite.
    # 
    def prepareSuite(self, suite_array):
        '''http://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing'''
        suites_list = []
        loader = unittest.TestLoader()
        for test_class in suite_array:
            suite = loader.loadTestsFromTestCase(test_class)
            suites_list.append(suite)
#             getSuite += self.addTestsToSuite(s)
        big_suite = unittest.TestSuite(suites_list)            
        return big_suite
#         loader = TestLoader()
#         suite = TestSuite(loader.loadTestsFromTestCase(Google_Search))
#         parser = SafeConfigParser()
#         base_driver_config_path = os.getcwd() + "\\..\\config\\base_driver_config.ini"
#         print "config_path is : ", base_driver_config_path
#         parser.read(base_driver_config_path)
#         class_name = parser.get('runConfig', 'runClass')
#         print "class_name is : ", class_name
 
        #to convert string to a Python class object - http://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
#         getSuite = self.addTestsToSuite(globals()[class_name])

#         class_name_split = class_name.split('.')
#         suite_name = class_name_split[0]
#         module_name = class_name_split[1]
#         test_name = class_name_split[2]
#         import_mod = "testScripts." + suite_name + "." + module_name  

        #http://stackoverflow.com/questions/769534/dynamic-loading-of-python-modules
#         structures = __import__(import_mod)
#         class_string_builder = "structures." + module_name + "." + test_name
#         class_obj = eval(class_string_builder)
        
#         getSuite = self.addTestsToSuite(structures.google_search.Google_Search)
#         runner = TextTestRunner(verbosity=2)
#         runner.run(suite)
#         unittest.TextTestRunner(verbosity=2).run(getSuite)
                
    #Use HTMLTestRunner to generate report for the executed cases    
    def executeSuite(self, suite_names):
        timestr = time.strftime("%Y%m%d%H%M%S")
        report_path = os.getcwd() + "\\..\\reports\\report_" + timestr + ".html"
        fp = open(report_path, "w")
        
        runner = HTMLTestRunner(
                stream=fp,
                verbosity=2,
                title='Report',
                description='Test Run Report'
                )
        
        runner.run(suite_names)
#         print "preparing report..."
     
    def main(self):
#         unittest_class = testScripts.SuiteD.google_search.Google_Search
#         test_suite = unittest.TestSuite()
#         test_suite.addTest(unittest.makeSuite(unittest_class))
#         self.executeSuite(test_suite)

        parser = SafeConfigParser()
        base_driver_config_path = os.getcwd() + "\\..\\config\\base_driver_config.ini"
#         print "config_path is : ", base_driver_config_path
        parser.read(base_driver_config_path)
        class_names = parser.get('runConfig', 'runClass')
#         print "class_names are : ", class_names
         
        class_names_list = class_names.split(',')
#         print class_names_list
         
        suite_arr = []
         
        for cname in class_names_list:
            complete_class_name = "testScripts." + cname
            suite_arr.append(eval(complete_class_name))
            
#             class_name_split = cname.split('.')
#             suite_name = class_name_split[0]
#             module_name = class_name_split[1]
#             test_name = class_name_split[2]
#             import_mod = "testScripts." + suite_name + "." + module_name
#             print "import_mod : ", import_mod
            #http://stackoverflow.com/questions/769534/dynamic-loading-of-python-modules
#             structures = __import__(import_mod)
#             print "structures :", structures
#             class_string_builder = "structures." + module_name + "." + test_name
#             print "class_string_builder : ", class_string_builder
#             class_obj = eval(class_string_builder)
#             print "class_obj :", class_obj
#             suite_arr.append(class_obj)
#         getSuite = self.addTestsToSuite(class_obj)
 
        print suite_arr
        prepared_suites = self.prepareSuite(suite_arr)
        self.executeSuite(prepared_suites)
        
         
bDriver = Base_Driver()
bDriver.main()