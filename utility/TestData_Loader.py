from utility.Excel_Utils import Excel_Utils
import os
import inspect

def loadTestData(class_obj):
    full_class_name = inspect.getmodule(class_obj).__name__
    test_path = getTestDataPath(full_class_name)
    excel_util = Excel_Utils(test_path, "Sheet1")
    return excel_util

def getTestDataPath(class_name):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    class_name_split = str(class_name).split('.')
    testdata_path = base_dir + "\\testScripts\\" + class_name_split[0] + "\\TestData.xlsx" 
    return testdata_path