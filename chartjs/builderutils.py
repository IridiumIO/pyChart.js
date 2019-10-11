import inspect
import json

class ExtChartUtils:

    @classmethod
    def merge(cls, dict1, dict2):
        if type(dict1) is not dict: dict1 = cls.clean(dict1)
        if type(dict2) is not dict: dict2 = cls.clean(dict2)
        return(dict1.update(dict2))

    @classmethod
    def cleanDict(cls, classObj):
        
        if classObj is None: return {}
        
        variables = vars(classObj)
        xn = dict([(n, variables[n]) for n in variables if (not n.startswith('_') and not inspect.isfunction(variables[n]))])
        return xn
    
    @classmethod
    def cleanClass(cls, classObj, retType=dict):
        
        if classObj is None: return []
        
        variables = vars(classObj)
        
        if retType is list:
            xn = [variables[n] for n in variables if (not n.startswith('_') and not inspect.isfunction(variables[n]))]
        else:
            xn = dict([(n, variables[n]) for n in variables if (not n.startswith('_') and not inspect.isfunction(variables[n]))])
        return xn
    
    @classmethod
    def BuildJSON(cls, parentClass, Dict):
        dict_ = cls.cleanDict(parentClass)
        cls.merge(dict_, Dict)
      
        return dict_



class FunctionsNotAllowedError(Exception):
    def __init__(self, msg=''):

        msg = ('Functions are not allowed in datasets. Use an in-line lambda function if necessary, or call the function from outside the chart class\n' 
               'ie:\n'
               '    ❌ def datapoint(self)\n'
               '           value = 24 * 45\n'
               '           return value\n'
               '\n'
               '    ✔  datapoint = 24 * 45\n'
               '\n'
               '    ✔  datapoint = functionOutsideChartClass(24, 45) \n'
            )
        super().__init__(msg)
        
