import copy
import openpyxl

# Extracting concept expression from a cell
class PhraseExtractor:

    def __init__(self, fullpath):
        self.FullPath = fullpath

        # Open workbook following a given path
        self.workbook = openpyxl.load_workbook(self.FullPath)

    # Read phrases with feature expressions for a cell and transform to list
    def read_phrase_from_cell(self, sheetname, in_column, in_row):

        # Open a worksheet with list of review sentence to be analyzed by different tools
        sheet = self.workbook.get_sheet_by_name(sheetname)

        # Reading a given review sentence from active worksheet and return as List
        cell_read = in_column + str(in_row)

        return sheet[cell_read].value.split(";") if isinstance(sheet[cell_read].value, str) else ""

    def read_value_from_cell(self, sheetname, in_column, in_row):

        # Open a worksheet with list of review sentence to be analyzed by different tools
        sheet = self.workbook.get_sheet_by_name(sheetname)

        # Reading a given review sentence from active worksheet and return as List
        cell_read = in_column + str(in_row)

        return sheet[cell_read].value


    def write_phrase_to_cell(self, sheetname, in_column, in_row, value):

        # Open a worksheet with list of review sentence to be analyzed by different tools
        sheet = self.workbook.get_sheet_by_name(sheetname)
        specific_cell = str(in_column) + str(in_row)
        sheet[specific_cell] = value

    def save_workbook(self):

        # Save extraction results to workbook
        self.workbook.save(self.FullPath)

if __name__ == '__main__':

    print("Hello Wolrd")
