import unittest
import os
import testScripts
import time
from utility.HTMLTestRunner import HTMLTestRunner
from utility.Worker_Thread import WorkerThread
# import inspect
import yaml
from utility.ParameterizedTestCase import ParameterizedTestCase
import threading, Queue
# from subprocess import Popen
from multiprocessing import Process, Queue

class SeleniumGrid_Distributed_Driver():
    
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
        
        print doc
        suite_arr = []
#         test_name = doc["runConfig"]["node1"]["tests"]["SuiteGrid"]

        '''
            Iterate through dictionary, and get class names and remote webdriver params 
        '''
        for k, v in doc.iteritems():
            for newK, newV in v.iteritems():
                ip = newV["ip"]
                print "ip is:", ip
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
        print "big suite is:", big_suite            
        return big_suite
    
    def executeSuites(self, suite_names):
        print "executing suites remotely..."
        timestr = time.strftime("%Y%m%d%H%M%S")
        report_path = os.getcwd() + "\\..\\reports\\report_" + timestr + ".html"
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
        for test in tests:
            time.sleep(1)
#             timestr = time.strftime("%Y%m%d%H%M%S")
#             report_path = os.getcwd() + "\\..\\reports\\report_" + timestr + ".html"
#             global file_handle
#             file_handle = open(report_path, "w")
        
            '''
                NOTE: Not passing file open stream to HTMLTestRunner during multiprocessing, as it
                closes the stream when creating a child process.
                Read this for solution - http://stackoverflow.com/questions/14899355/python-multiprocessing-valueerror-i-o-operation-on-closed-file 
            '''
            runner = HTMLTestRunner(
                stream=report_path,
                verbosity=2,
                title='Report',
                description='Test Run Report'
            )
            
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
            p = Process(target=runner.run, args=(test, report_path))
            jobs.append(p)
            
        for i in jobs:
            i.start()
            
        for i in jobs:
            i.join()
#             p.start()
#             p.join() # this blocks until the process terminates
#             result = queue.get()
#             print result
        
        
#         ThreadCount = 3;
#         QueueSize = 10;
#         
#         start = time.time()
#         jobQueue = Queue.Queue(QueueSize);
#         threadsList = [];
#         for i in range(ThreadCount):
#             t = WorkerThread(str(i), jobQueue);
#             threadsList.append(t);
#             t.start();
# 
#         tests = suite_names
#         for test in tests:
#             jobQueue.put((test, runner.run(test)));

        # marking end of jobQueue, one marker per thread
#         for i in range(ThreadCount):
#             jobQueue.put((None, None));
# 
#         for t in threadsList:
#             while t.isAlive():
#                 time.sleep(1);

#         print "*" * 50
#         print "Time taken: %s minutes" % ((time.time() - start) /60)

#         result = runner.run(suite_names)
#         return result
    
    def main(self):
        '''TODO: Prepare a yml for hub, nodes and tests to be executed on those'''
        suite_array = self.getSuiteFromConfig()
        prepared_suites = self.prepareSuites(suite_array)
        self.executeSuites(prepared_suites)
        '''
            Need to implement rerun failures capability
        '''
        
# grid = SeleniumGrid_Distributed_Driver()
# grid.main()