import unittest
import os
import testScripts
import time
from utility.HTMLTestRunner import HTMLTestRunner
# import inspect
import yaml
from utility.ParameterizedTestCase import ParameterizedTestCase

class SeleniumGrid_Distributed_Driver():
    
    '''
        1. Prepare suite array in the form that Unit Test Runner likes
        2. Store corresponding ip, port, browser information for that test - 
            
            Use this - http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases
            
        3. When that test is invoked, add a method in Common_Actions to fetch port, browser and ip information
        4. Form the remote url and desired cap instance there
        5. Instantiate the remote web driver instance, and get going!!
    '''
    
    def getSuiteFromConfig(self):
        grid_driver_config_path = os.getcwd() + "\\..\\config\\grid_driver_config.yaml"
        with open(grid_driver_config_path, 'r') as f:
            doc = yaml.load(f)
        
        print doc
        suite_arr = []
#         test_name = doc["runConfig"]["node1"]["tests"]["SuiteGrid"]

        '''
            Iterate through dictionary, and get class names and remote webdriver params 
        '''
        for k, v in doc.iteritems():
            for newK, newV in v.iteritems():
                ip = newV["ip"]
                tests = newV["tests"]
                port = newV["port"]
                browser = newV["browser"]
                '''
                    Store parsed suite names in this format:
                    {'class_names' : complete_class_name, 'webdriver_params' : params}
                    Then, push above into list
                    Finally you should have something like this ("Array of Hash" OR "List of Dictionary"):
                    [{'class_names' : complete_class_name, 'webdriver_params' : [params]}, {'class_names' : complete_class_name, 'webdriver_params' : [params]}] 
                '''
                complete_class_name = "testScripts." + tests
                params = [ip, port, browser]
                hash = {'class_names' : eval(complete_class_name), 'webdriver_params' : params}
                suite_arr.append(hash)
        
        print "suite arr is:", suite_arr
        return suite_arr
    
    def prepareSuites(self, suite_array):
        print "preparing suites for distributed execution..."
        suites_list = []
        
        '''
            Iterate through the suite array:
            [{'class_names' : complete_class_name, 'webdriver_params' : [params]}, {'class_names' : complete_class_name, 'webdriver_params' : [params]}]
        '''
        for arr in suite_array:
#             print "arr is:", arr
            suite = ParameterizedTestCase.parameterize(arr["class_names"], param=arr["webdriver_params"])
            suites_list.append(suite)
            
#             for k, v in arr.iteritems():
#                 print "key is:", k
#                 print "value is:", v
#                 if k == "webdriver_params":
#                     webdriver_params = v
#                 print "webdriver params are:", webdriver_params
#                 suite = ParameterizedTestCase.parameterize(v["class_names"], param=webdriver_params)
#                 suites_list.append(suite)
        
        big_suite = unittest.TestSuite(suites_list)
        print "big suite is:", big_suite            
        return big_suite
    
    def executeSuites(self, suite_names):
        print "executing suites remotely..."
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
    
    def main(self):
        '''TODO: Prepare a yml for hub, nodes and tests to be executed on those'''
        suite_array = self.getSuiteFromConfig()
        prepared_suites = self.prepareSuites(suite_array)
        self.executeSuites(prepared_suites)
        '''
            Need to implement rerun failures capability
        '''
        
grid = SeleniumGrid_Distributed_Driver()
grid.main()