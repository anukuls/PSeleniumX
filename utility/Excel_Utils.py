import openpyxl
import logging
import utility.Log_Manager


class Excel_Utils():
    
    def __init__(self, path, sheetname):
        self.logger = logging.getLogger("utility." + self.__class__.__name__)
        self.workbook = openpyxl.load_workbook(path)
        self.worksheet = self.workbook.get_sheet_by_name(sheetname)
    
    def getCellData(self, class_name, column_name):
        self.logger.debug("Get Cell Data : function - %s , column name - %s" % (class_name, column_name))
        
        try:
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
                
            val = sheet.cell(row=r, column=c).value
            self.logger.debug("Output of getCellData(%s, %s) is : %s" %(class_name, column_name, val))
        except Exception as e:
            self.logger.exception("Error from getCellData is : %s" % e)
            raise
            
        return val