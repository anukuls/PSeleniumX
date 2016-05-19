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
from multiprocessing import Process
import socket
import logging
import utility.Log_Manager
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ConfigParser import SafeConfigParser

class SeleniumGrid_Distributed_Driver(object):
    
    '''
        1. Prepare suite array in the form that Unit Test Runner likes
        2. Store corresponding ip, port, browser information for that test - 
            
            Use this - http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases
            
        3. When that test is invoked, add a method in Common_Actions to fetch port, browser and ip information
        4. Form the remote url and desired cap instance there
        5. Instantiate the remote web driver instance, and get going!!
    '''

    def __init__(self):
        self.logger = logging.getLogger("runManager." + self.__class__.__name__)
        self.logger.info("Beginning execution of Selenium Grid Distributed Driver")
    
    def getSuiteFromConfig(self):
        try:
            grid_driver_config_path = os.getcwd() + "\\..\\config\\grid_driver_config.yaml"
            with open(grid_driver_config_path, 'r') as f:
                doc = yaml.load(f)
        
            suite_arr = []
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
                    
                    params = [ip, port, browser]
                    test_hash = {'class_names' : tests, 'webdriver_params' : params}
                    suite_arr.append(test_hash)
            self.logger.debug("Distributed Suite to be executed %s" % suite_arr)            
            
        except Exception as e:
            self.logger.exception("Error from getSuiteFromConfig : %s" % e)
            raise
            
        return suite_arr
    
    def prepareSuites(self, suite_array):
        
        self.logger.info("Preparing suites for distributed execution")
        suites_list = []
        
        '''
            Iterate through the suite array:
            [{'class_names' : complete_class_name, 'webdriver_params' : [params]}, {'class_names' : complete_class_name, 'webdriver_params' : [params]}]
        '''
        try:
            for arr in suite_array:
                
                suite = ParameterizedTestCase.parameterize(arr["class_names"], param=arr["webdriver_params"])
                '''
                    Let the suite object be created in ParameterizedTestCase module as one.  Multiple cases
                    belonging to a single IP Address would need to be appended there as well, and finally appended
                    here to form the bigger suite of all remote machines
                '''
                suites_list.append(suite)
        except Exception as e:
            self.logger.exception("Error from prepareSuites : %s" % e)
            raise
            
        big_suite = unittest.TestSuite(suites_list)    
        return big_suite
        
    def executeSuites(self, suite_names):
        self.logger.info("Executing suites on remote machines parallely")
        timestr = time.strftime("%Y%m%d%H%M%S")
        report_path = os.getcwd() + "\\..\\reports\\report_" + timestr + ".html"
        log_path = os.getcwd() + "\\..\\logs\\log_" + timestr + ".log"
        
        '''
            TODO: Need to figure out a way to run HTMLTestRunner as a thread,
            and spawn one process per remote machine.  This will utilize grid's
            capability to run tests in parallel
        '''
        tests = suite_names
        jobs = []
        
        runner = HTMLTestRunner(
                stream=report_path,
                verbosity=2,
                title='Report',
                description='Test Run Report',
            )
        
        self.logger.info("Starting distributed execution")
        
        try:
            
            for test in tests:
                time.sleep(1)
                '''
                    NOTE: Not passing file open stream to HTMLTestRunner during multiprocessing, as it
                    closes the stream when creating a child process.
                    Read this for solution - http://stackoverflow.com/questions/14899355/python-multiprocessing-valueerror-i-o-operation-on-closed-file 
                '''
                
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
                p = Process(target=runner.threadedRun, args=(test, report_path, log_path))
                jobs.append(p)
                
            for i in jobs:
                i.start()    
    
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
            self.logger.debug("Consolidated result of distributed run is : %s" % result)
        except Exception as e:
            self.logger.exception("Error from executeSuites is : %s" % e)
            raise
        
        return result
    
    def prepareSuiteForMasterRerun(self, suite_array):
        self.logger.info("Preparing suite for rerun of failure tests")
        '''
            For rerun, use the hub machine to rerun all the failed tests.  Pass as following suite array:
            [{'class_names' : 'SuiteGrid.google_search_grid.Google_Search', 'webdriver_params' : ['172.18.95.28', 4444, 'firefox']}]
        '''
        machine_ip = socket.gethostbyname(socket.gethostname())
        
        new_suite_array = []
        
        try:
            for sa in suite_array:
                splitter = sa.split('.')
                splitter.pop(0)
                test_name = ".".join(splitter)
                new_suite_array.append(test_name)
            
            suite_string = ""
            for test in new_suite_array:
                suite_string = suite_string + test + ","
                
            suite_string = suite_string[:-1]
        except Exception as e:
            self.logger.exception("Error from prepareSuiteForMasterRerun is : %s" % e)
            raise
        
        '''TODO: Pick browser name from grid_driver_config.yaml, remove hardcoding'''
        master_suite_array = [{'class_names' : suite_string , 'webdriver_params' : ["127.0.0.1", 4444, 'firefox']}]
        self.logger.debug("failed suite to be executed is : %s" % master_suite_array)
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
            suites_list.append(suite)
        
        big_suite = unittest.TestSuite(suites_list)                                
        return big_suite
    
    def executeSuite(self, suite_names):
        self.logger.info("Rerunning Failures : %s" % suite_names)
        timestr = time.strftime("%Y%m%d%H%M%S")
        report_path = os.getcwd() + "\\..\\reports\\rerun_reports\\report_" + timestr + ".html"
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
            self.logger.exception("Error from Rerun executeSuite : %s" % e)
            raise
            
        return result
    
    def getFailures(self, result):
        failed_tcs = result["fail_classes"]
        error_tcs = result["error_classes"]
        all_failures = failed_tcs + error_tcs
        self.logger.debug("failure tests are : %s" % all_failures)
        return all_failures
    
    def rerunFailures(self, failure_array):
        prepared_failure_suite = self.prepareSuite(failure_array)
        result = self.executeSuite(prepared_failure_suite)
        return result
        
    '''
        To Avoid send email authentication errors from gmail, goto https://www.google.com/settings/security/lesssecureapps
        and TURN ON access for less secure apps.  The code below will work then
    '''
    def sendEmail(self, final_result):
        self.logger.info("Sending result email to the desired recipients")
#         to = 'opencti2@gmail.com'
#         gmail_user = 'opencti2@gmail.com'
#         gmail_pwd = 'smoke123!' 
        
        parser = SafeConfigParser()
        email_config_path = os.getcwd() + "\\..\\config\\email_config.ini"
        
        parser.read(email_config_path)
        to = parser.get('emailConfig', 'recipients')
        recipient_arr = to.split(',')
                 
        gmail_user = parser.get('emailConfig', 'from_user')
        gmail_pwd = parser.get('emailConfig', 'from_pwd')
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Test Run Result"
        msg['From'] = gmail_user
        msg['To'] = ", ".join(recipient_arr)
        
        # Create the body of the message
        '''
            1. Send html email - http://stackoverflow.com/questions/882712/sending-html-email-using-python
            2. To pass variables within html - http://stackoverflow.com/questions/13208212/python-variable-in-an-html-email-in-python
        '''
        count = final_result["count"]
        passed = final_result["passed"]
        failed = final_result["failed"]
        html = """\
            <html>
              <head></head>
              <body>
                <p>
                   <b>Count = {count}</b><br>
                   <b>Pass = {passed}</b><br>
                   <b>Fail = {failed}</b><br>
                </p>
              </body>
            </html>
        """.format(**locals())
        
        # Record the MIME types
        part1 = MIMEText(html, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1) 
        
        '''Pick to (authentication info) and recipients information from an xml file'''
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com",587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            smtpserver.sendmail(gmail_user, recipient_arr, msg.as_string())
            self.logger.info("Email sent to desired recipients - %s" % to)
        except Exception as e:
            self.logger.exception("Unable to send email.  Error is : %s" % e)
            '''No need to raise exception'''
        finally:
            smtpserver.close();
    
    def main(self):
        suite_array = self.getSuiteFromConfig()
        prepared_suites = self.prepareSuites(suite_array)
        consolidated_result = self.executeSuites(prepared_suites)
        self.logger.info("Consolidated results are : %s" % consolidated_result)
        all_failures = self.getFailures(consolidated_result)
        
        if len(all_failures) == 0:
            self.logger.info("No failures found, hence no need to rerun")
        else:
            rerun_result = self.rerunFailures(all_failures)
            self.logger.debug("rerun_result is : %s" % rerun_result)
            rerun_result_failure_count = rerun_result.failure_count
            rerun_result_error_count = rerun_result.error_count
            rerun_result_success_count = rerun_result.success_count 
        '''
            Get Final Result after rerun and send result to stakeholders
            Send body as an html
        '''
        final_result = {}
        final_result["count"] = consolidated_result["count"]
        final_result["passed"] = consolidated_result["passed"] + rerun_result_success_count
        final_result["failed"] = rerun_result_failure_count + rerun_result_error_count
        
        '''TODO: Send email only if send_email flag is set to true in email_config.ini'''
        self.sendEmail(final_result)

'''http://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing'''        
if __name__ == '__main__':
    grid = SeleniumGrid_Distributed_Driver()
    grid.main()        