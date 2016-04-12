import openpyxl


class Excel_Utils():
    
    def __init__(self, path, sheetname):
#         print "initializing workbook"
        self.workbook = openpyxl.load_workbook(path)
        self.worksheet = self.workbook.get_sheet_by_name(sheetname)
    
    def getCellData(self, class_name, column_name):
#         print "fetch data"
        sheet = self.worksheet
        header = sheet.rows[0]
        r = 0
        c = 0
        for index, h in enumerate(header):
            cell_value = h.value
            if cell_value == column_name:
                c = index + 1
                break

        for index, row in enumerate(sheet.rows[0:]):
            for cell in row:
                if cell.value == class_name.__name__:
                    r = index + 1
                    break
                break
        
#         print "row index :", r
#         print "col index :", c
            
        val = sheet.cell(row=r, column=c).value
        return val
        

# path = "C:/Users/anukul.singhal/git/PSeleniumX/testScripts/SuiteC/TestData.xlsx"
# sheet = "Sheet1"        
# excel = Excel_Utils(path, sheet)
# cell_value = excel.getCellData("Google_Search", "Search_String")
# print "cell value :", cell_value