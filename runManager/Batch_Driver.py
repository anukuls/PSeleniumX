import unittest
import os
import testScripts
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from utility.HTMLTestRunner import HTMLTestRunner
import inspect
import logging
import utility.Log_Manager

class Batch_Driver():
    
    def __init__(self):
        self.logger = logging.getLogger("runManager." + self.__class__.__name__)
        self.logger.info("Beginning execution of Batch Driver")
    
    def parseXMLForSuites(self, xml_file):
        class_names_list = []
        
        try:
            dtree = xml.dom.minidom.parse(xml_file)
            suite = dtree.documentElement
            tests = suite.getElementsByTagName("class")
            for test in tests:
                class_names = test.getElementsByTagName('name')
                for cname in class_names:
                    class_names_list.append(str(cname.childNodes[0].data))
        except Exception as e:
            self.logger.exception("Error from parseXMLForSuites is : %s" % e)
            raise
            
        return class_names_list
    
    '''
        Define batch config in the form of an xml, parse data from it.
        Also define a rerun param to determine if the failed tests need to 
        be run automatically or not.
    '''
    def getSuiteFromConfig(self):
        batch_driver_config_path = os.getcwd() + "\\..\\config\\batch_driver_config.xml"         
        class_names_list = self.parseXMLForSuites(batch_driver_config_path)         
        suite_arr = []
    
        try:      
            for cname in class_names_list:
                complete_class_name = "testScripts." + cname
                suite_arr.append(eval(complete_class_name))
        except Exception as e:
            self.logger.exception("Error from getSuiteFromConfig is : %s" % e)
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
        self.logger.debug("Suites to be executed : %s" % big_suite)                      
        return big_suite

    #Use HTMLTestRunner to generate report for the executed cases    
    def executeSuite(self, suite_names):
        timestr = time.strftime("%Y%m%d%H%M%S")
        
        '''TODO: Add a rerun flag which will set report_path to use reports/rerun folder when true'''
        report_path = os.getcwd() + "\\..\\reports\\report_" + timestr + ".html"
        
        self.logger.info("Executing suites in batch mode")
        try:
            fp = open(report_path, "w")
            
            runner = HTMLTestRunner(
                    stream=fp,
                    verbosity=2,
                    title='Report',
                    description='Test Run Report'
                    )
            
            result = runner.run(suite_names)
        except Exception as e:
            self.logger.exception("Error from executeSuite is : %s" % e)
            raise
            
        return result
    
    def getFailures(self, result):
        '''http://stackoverflow.com/questions/284043/outputting-data-from-unit-test-in-python'''        
        all_failed_classes = []
        all_errors = result.errors
        error_classes = []
        for err in all_errors:
            err_cls_name = err[0].__class__.__name__
            err_mod_name = inspect.getmodule(err[0].__class__).__name__
            full_err_class_name = "testScripts." + str(err_mod_name) + "." + str(err_cls_name)             
            error_classes.append(eval(full_err_class_name))
 
        all_failures = result.failures
        failure_classes = []
        for failure in all_failures:
            fail_cls_name = failure[0].__class__.__name__
            fail_mod_name = inspect.getmodule(failure[0].__class__).__name__
            full_fail_class_name = "testScripts." + str(fail_mod_name) + "." + str(fail_cls_name)
            failure_classes.append(eval(full_fail_class_name))
 
        all_failed_classes = error_classes + failure_classes
        
        self.logger.debug("All failed tests : %s" % all_failed_classes)
         
        return all_failed_classes    
        
    def rerunFailures(self, failure_array):
        self.logger.info("Rerunning failure scripts")
        prepared_failure_suite = self.prepareSuite(failure_array)
        self.executeSuite(prepared_failure_suite)
     
    def main(self):
        suite_array = self.getSuiteFromConfig()
        prepared_suites = self.prepareSuite(suite_array)
        results = self.executeSuite(prepared_suites)
        failures = self.getFailures(results)
        
        if len(failures) == 0:
            self.logger.info("No failures found, hence no need to rerun")
        else:
            self.rerunFailures(failures)      
         
batchDriver = Batch_Driver()
batchDriver.main()