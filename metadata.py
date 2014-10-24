# metadata.py
"""
File containing metadata information for WW2100 model run
"""
class UnknownFileType(BaseException):
    pass

AltScenarios = ["Ref","LowClim","HighClim","FireSuppress","UrbExpand","HighPop","FullCostUrb", "EarlyReFill"]

def define_model_run(name):
    import xlrd
    model_book = xlrd.open_workbook('master file.xls')
    if name == "first": 
        Case = str(model_book.sheet_by_index(0).col_values(0)[1])      #find the reference model type
    else:
        Case = str(name)
        
    if "Ref_Run0" in Case:
        model = 'Reference (MIROC)'
        short_name = 'Ref'
    elif "LowClim" in Case:  
        model = 'Low Climate Change (GFDL)'
        short_name = 'LowClim'
    elif "FireSuppress" in Case:  
        model = 'Upland Fire Suppression'
        short_name = 'FireSuppress'
    elif "HighClim" in Case:  
        model = 'High Climate Change (Hadley)'
        short_name = 'HighClim'
    elif "UrbExpand" in Case:  
        model = "Relaxed Urban Expansion"
        short_name = 'UrbExpand'
    elif "HighPop" in Case:  
        model = "High Population Growth"
        short_name = 'HighPop'
    elif "FullCostUrb" in Case:  
        model = "Full Cost Urban"
        short_name = 'FullCostUrb'
    elif "EarlyReFill" in Case:
        model = "Early Refill"
        short_name = 'EarlyReFill'
    else:
        raise UnknownFileType()
    return model, short_name

model_run, short_name = define_model_run("first")
##print model_run
