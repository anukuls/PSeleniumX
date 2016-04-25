import unittest
import os
import testScripts
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from utility.HTMLTestRunner import HTMLTestRunner
import inspect

class Batch_Driver():
    
    def parseXMLForSuites(self, xml_file):
        class_names_list = []
        dtree = xml.dom.minidom.parse(xml_file)
        suite = dtree.documentElement
        tests = suite.getElementsByTagName("class")
        for test in tests:
            class_names = test.getElementsByTagName('name')
            for cname in class_names:
                class_names_list.append(str(cname.childNodes[0].data))
            
        return class_names_list
    
    '''
        Define batch config in the form of an xml, parse data from it.
        Also define a rerun param to determine if the failed tests need to 
        be run automatically or not.
    '''
    def getSuiteFromConfig(self):
#         parser = SafeConfigParser()
        batch_driver_config_path = os.getcwd() + "\\..\\config\\batch_driver_config.xml"
#         parser.read(base_driver_config_path)
#         class_names = parser.get('runConfig', 'runClass')         
        class_names_list = self.parseXMLForSuites(batch_driver_config_path)
#         class_names_list = class_names.split(',')         
        suite_arr = []
         
        for cname in class_names_list:
            complete_class_name = "testScripts." + cname
            suite_arr.append(eval(complete_class_name))
             
        return suite_arr
    
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
        
        result = runner.run(suite_names)
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
        print "all failed classes:", all_failed_classes
         
        return all_failed_classes    
        
    def rerunFailures(self, failure_array):
        print "rerunning failure scripts..."
        prepared_failure_suite = self.prepareSuite(failure_array)
        self.executeSuite(prepared_failure_suite)
     
    def main(self):
        suite_array = self.getSuiteFromConfig()
        prepared_suites = self.prepareSuite(suite_array)
        results = self.executeSuite(prepared_suites)
        failures = self.getFailures(results)
        
        if len(failures) == 0:
            print "No failures found, hence no need to rerun"
        else:
            self.rerunFailures(failures)      
         
batchDriver = Batch_Driver()
batchDriver.main()