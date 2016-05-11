import unittest
import os
import testScripts
import time
from utility.HTMLTestRunner import HTMLTestRunner
# from utility.Worker_Thread import WorkerThread
# import inspect
import yaml
from utility.ParameterizedTestCase import ParameterizedTestCase
# import threading, Queue
# from subprocess import Popen
from multiprocessing import Process, Queue
import socket
# import multiprocessing

class SeleniumGrid_Distributed_Driver(object):
    
    '''
        1. Prepare suite array in the form that Unit Test Runner likes
        2. Store corresponding ip, port, browser information for that test - 
            
            Use this - http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases
            
        3. When that test is invoked, add a method in Common_Actions to fetch port, browser and ip information
        4. Form the remote url and desired cap instance there
        5. Instantiate the remote web driver instance, and get going!!
    '''
    
#     file_handle = None
    
    def getSuiteFromConfig(self):
        grid_driver_config_path = os.getcwd() + "\\..\\config\\grid_driver_config.yaml"
        with open(grid_driver_config_path, 'r') as f:
            doc = yaml.load(f)
        
#         print doc
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
                
#                 test_list = tests.split(',')
                params = [ip, port, browser]
#                 complete_class_name = "testScripts." + tests
#                 test_hash = {'class_names' : eval(complete_class_name), 'webdriver_params' : params}
                test_hash = {'class_names' : tests, 'webdriver_params' : params}
                suite_arr.append(test_hash)
#                 for test in test_list:
#                     complete_class_name = "testScripts." + test
#                     test_hash = {'class_names' : eval(complete_class_name), 'webdriver_params' : params}
#                     suite_arr.append(test_hash)
        
#         print "suite arr is:", suite_arr
        return suite_arr
    
    def prepareSuites(self, suite_array):
#         print "preparing suites for distributed execution..."
        suites_list = []
        
        '''
            Iterate through the suite array:
            [{'class_names' : complete_class_name, 'webdriver_params' : [params]}, {'class_names' : complete_class_name, 'webdriver_params' : [params]}]
        '''
        for arr in suite_array:
#             print "arr is:", arr
                
            suite = ParameterizedTestCase.parameterize(arr["class_names"], param=arr["webdriver_params"])
            '''
                Let the suite object be created in ParameterizedTestCase module as one.  Multiple cases
                belonging to a single IP Address would need to be appended there as well, and finally appended
                here to form the bigger suite of all remote machines
            '''
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
#         print "big suite is:", big_suite            
        return big_suite
    
#     def __call__(self, test, runner, report_path, out_que):
#         runner.run(test, report_path, out_que)
        
    def executeSuites(self, suite_names):
#         print "executing suites remotely..."
        timestr = time.strftime("%Y%m%d%H%M%S")
        report_path = os.getcwd() + "\\..\\reports\\report_" + timestr + ".html"
        log_path = os.getcwd() + "\\..\\logs\\log_" + timestr + ".log"
#         fp = open(report_path, "w")
#         
#         runner = HTMLTestRunner(
#                 stream=fp,
#                 verbosity=2,
#                 title='Report',
#                 description='Test Run Report'
#                 )
        
        '''
            TODO: Need to figure out a way to run HTMLTestRunner as a thread,
            and spawn one process per remote machine.  This will utilize grid's
            capability to run tests in parallel
        '''
        
#         processes = []
#         for test in tests:
#             processes.append(Popen('python %s' % test, shell=True))

#         queue = Queue()
        
        tests = suite_names
        jobs = []
#         manager = multiprocessing.Manager()
#         out_queue = Queue()
#         queues = []
        
        runner = HTMLTestRunner(
                stream=report_path,
                verbosity=2,
                title='Report',
                description='Test Run Report',
            )
        
        for test in tests:
            time.sleep(1)
#             q = Queue()
#             timestr = time.strftime("%Y%m%d%H%M%S")
#             report_path = os.getcwd() + "\\..\\reports\\report_" + timestr + ".html"
#             global file_handle
#             file_handle = open(report_path, "w")
        
            '''
                NOTE: Not passing file open stream to HTMLTestRunner during multiprocessing, as it
                closes the stream when creating a child process.
                Read this for solution - http://stackoverflow.com/questions/14899355/python-multiprocessing-valueerror-i-o-operation-on-closed-file 
            '''
#             runner = HTMLTestRunner(
#                 out_queue,
#                 stream=report_path,
#                 verbosity=2,
#                 title='Report',
#                 description='Test Run Report',
#             )
            
            '''
                TODO: Find out way to create consolidated report rather than one report per test
                1. Each time generate_report is called, it opens a new instance of file in 'w' (write) mode
                2. Need to open file in append mode so that it creates one full report
            '''
            
            '''
                NOTE: Currently, execution is happening as follows:
                1. Let's say remote machine 1 = 1 test to execute, remote machine 2 = 2 tests to execute
                2. Execution starts in parallel on remote machine 1 and remote machine 2
                3. On remote machine 2, the 2 tests that are to be run also execute in parallel.  This will give
                   problem when an application has cache issues, and you are required to login with a different user
                   everytime.  
                4. Based on problem 3, need to implement solution such that every remote machine executes tests
                   sequentially.
                5. Final verdict - Parallel execution on remote machines, sequential execution of tests configured 
                   on each remote machine
                   
                IDEA 1 - If I group tests by remote machines IP Address, and group the tests to be executed on that
                machine as 1 suite, then we would be effectively running 1 process lesser, and runner.run would 
                execute that suite as 1.  Execution should happen sequentially.
            '''
#             p = Process(target=runner.run, args=(test, report_path, out_queue))
            p = Process(target=runner.threadedRun, args=(test, report_path, log_path))
            jobs.append(p)
            
        for i in jobs:
            i.start()    
#         print "output of runner.run:", q.get()

#         while not out_queue.empty():
#         print "queue is not empty..."
#         print out_queue.get()
#         queues.append(out_queue.get())
            
        for i in jobs:
            i.join()
#         
        '''
            Use Multiprocessing Queues to capture return value of a function, and iterate through the Queues to get each
            Result object.  Process that result object and create a total result report which will be passed to the 
            generateReport function
            1. Need to capture return value of runner.run and append it for each test run
            2. Create total result here
            3. Call generateReport function of HTMLTestRunner to generated one consolidated report for the report path
            
            Somehow, unable to capture the return output of runner.run through multiprocessing
            Getting PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed
            HACKISH WORKAROUND: 
            1. Whenever runner.run is called, store the results in a log file locally, and append to that file
            2. When the run is complete, read from the flat file, and then try to construct a neat consolidated report
            3. This way we would be able to process the result
        '''            
        runner.generateConsolidatedReport(report_path, log_path)
        result = runner.readResultFromLogpath(log_path)
        return result
    
    def prepareSuiteForMasterRerun(self, suite_array):
#         print "preparing suite for master rerun..."
        '''
            For rerun, use the hub machine to rerun all the failed tests.  Pass as following suite array:
            [{'class_names' : 'SuiteGrid.google_search_grid.Google_Search', 'webdriver_params' : ['172.18.95.28', 4444, 'firefox']}]
        '''
        machine_ip = socket.gethostbyname(socket.gethostname())
#         print "machine ip:", machine_ip
        
        new_suite_array = []
        for sa in suite_array:
            splitter = sa.split('.')
            splitter.pop(0)
            test_name = ".".join(splitter)
            new_suite_array.append(test_name)
        
#         print "new suite array :", new_suite_array
        
        suite_string = ""
        for test in new_suite_array:
            suite_string = suite_string + test + ","
            
        suite_string = suite_string[:-1]
        
        master_suite_array = [{'class_names' : suite_string , 'webdriver_params' : [machine_ip, 4444, 'firefox']}]
        return master_suite_array
        
    
    '''This method is only for rerun on one of the node machines'''
    def prepareSuite(self, suite_arr):
        suites_list = []
        suite_array = self.prepareSuiteForMasterRerun(suite_arr)
        
        '''
            Iterate through the suite array:
            [{'class_names' : complete_class_name, 'webdriver_params' : [params]}, {'class_names' : complete_class_name, 'webdriver_params' : [params]}]
        '''
        for arr in suite_array:    
            suite = ParameterizedTestCase.parameterize(arr["class_names"], param=arr["webdriver_params"])
            '''
                Let the suite object be created in ParameterizedTestCase module as one.  Multiple cases
                belonging to a single IP Address would need to be appended there as well, and finally appended
                here to form the bigger suite of all remote machines
            '''
            suites_list.append(suite)
        
        big_suite = unittest.TestSuite(suites_list)
#         print "big suite is:", big_suite            
                    
        return big_suite

    #Use HTMLTestRunner to generate report for the executed cases    
    def executeSuite(self, suite_names):
        timestr = time.strftime("%Y%m%d%H%M%S")
        report_path = os.getcwd() + "\\..\\reports\\rerun_reports\\report_" + timestr + ".html"
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
        failed_tcs = result["fail_classes"]
        error_tcs = result["error_classes"]
        all_failures = failed_tcs + error_tcs
        return all_failures
    
    def rerunFailures(self, failure_array):
#         print "rerunning failure scripts..."
        prepared_failure_suite = self.prepareSuite(failure_array)
        self.executeSuite(prepared_failure_suite)
    
    def main(self):
        '''TODO: Prepare a yml for hub, nodes and tests to be executed on those'''
        suite_array = self.getSuiteFromConfig()
        prepared_suites = self.prepareSuites(suite_array)
        consolidated_result = self.executeSuites(prepared_suites)
        all_failures = self.getFailures(consolidated_result)
        '''
            Need to implement rerun failures capability
        '''
        if len(all_failures) == 0:
            print "No failures found, hence no need to rerun"
        else:
            self.rerunFailures(all_failures)
        
if __name__ == '__main__':
    grid = SeleniumGrid_Distributed_Driver()
    grid.main()        
# grid = SeleniumGrid_Distributed_Driver()
# grid.main()