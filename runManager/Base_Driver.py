import unittest
import os
import testScripts
import time
from ConfigParser import SafeConfigParser
from utility.HTMLTestRunner import HTMLTestRunner
import logging
import utility.Log_Manager
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
     
    def __init__(self):
        self.logger = logging.getLogger("runManager." + self.__class__.__name__)
        self.logger.info("Beginning execution of Base Driver")
        
    def parseIniForSuites(self):
        parser = SafeConfigParser()
        suite_arr = []
        base_driver_config_path = os.getcwd() + "\\..\\config\\base_driver_config.ini"
        
        try:
            parser.read(base_driver_config_path)
            class_names = parser.get('runConfig', 'runClass')
             
            class_names_list = class_names.split(',')
             
            for cname in class_names_list:
                complete_class_name = "testScripts." + cname
                suite_arr.append(eval(complete_class_name))
        except Exception as e:
            self.logger.exception("Error from parseIniForSuites is : %s" % e)
            raise
            
        return suite_arr
     
    def prepareSuite(self, suite_array):
        '''http://stackoverflow.com/questions/5360833/how-to-run-multiple-classes-in-single-test-suite-in-python-unit-testing'''
        suites_list = []
        
        try:
            loader = unittest.TestLoader()
            for test_class in suite_array:
                suite = loader.loadTestsFromTestCase(test_class)
                suites_list.append(suite)
        except Exception as e:
            self.logger.exception("Error from prepareSuite is : %s" % e)
            raise

        big_suite = unittest.TestSuite(suites_list)            
        return big_suite
                
    #Use HTMLTestRunner to generate report for the executed cases    
    def executeSuite(self, suite_names):
        timestr = time.strftime("%Y%m%d%H%M%S")
        report_path = os.getcwd() + "\\..\\reports\\report_" + timestr + ".html"
        
        try:
            fp = open(report_path, "w")
            
            runner = HTMLTestRunner(
                    stream=fp,
                    verbosity=2,
                    title='Report',
                    description='Test Run Report'
                    )
            
            runner.run(suite_names)
        except Exception as e:
            self.logger.exception("Error from executeSuite is : %s" % e)
            raise
     
    def main(self):
        suite_arr = self.parseIniForSuites() 
        self.logger.info("Tests to be executed are : %s" % suite_arr)
        prepared_suites = self.prepareSuite(suite_arr)
        self.executeSuite(prepared_suites)
        
bDriver = Base_Driver()
bDriver.main()