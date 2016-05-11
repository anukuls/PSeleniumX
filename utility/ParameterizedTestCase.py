import unittest
import testScripts

class ParameterizedTestCase(unittest.TestCase):
    
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParameterizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parameterize(testcase_klasses, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        "ANUKUL: Custom implementation for Selenium Grid parallel run"
        suite = unittest.TestSuite()
        klass_string_list = testcase_klasses.split(',')
        for klass in klass_string_list:
            complete_class_name = "testScripts." + klass
            class_name = eval(complete_class_name)
            testloader = unittest.TestLoader()
            testnames = testloader.getTestCaseNames(class_name)
            for name in testnames:
                suite.addTest(class_name(name, param=param))
        "ANUKUL"
#         testloader = unittest.TestLoader()
#         testnames = testloader.getTestCaseNames(testcase_klass)
        
        '''
            TODO: Need to form the group suite here based on IP Address, and return that suite.
            Currently, it creates one TestSuite per TestCase.
        '''
#         suite = unittest.TestSuite()
#         for name in testnames:
#             suite.addTest(testcase_klass(name, param=param))
#         print "parameterized suite is:", suite
        return suite