# metadata.py
"""
File containing metadata information for WW2100 model run
"""
class UnknownFileType(BaseException):
    pass

def define_model_run(name):
    import xlrd
    model_book = xlrd.open_workbook('master file.xls')
    if name == "first": 
        Case = str(model_book.sheet_by_index(0).col_values(0)[1])      #find the reference model type
    else:
        Case = str(name)
        
    if len(Case) > 0:
        model = 'Example data set'
        short_name = 'example'
    else:
        raise UnknownFileType()
    return model, short_name

model_run, short_name = define_model_run("first")
##print model_run
