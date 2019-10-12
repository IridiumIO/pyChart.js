import inspect
import json
from enum import Enum


class ChartType(Enum):

    Line = 'line'
    Bar = 'bar'
    Pie = 'pie'
    Doughnut = 'doughnut'
    Radar = 'radar'
    PolarArea = 'polarArea'
    HorizontalBar = 'horizontalBar'
    Mixed = 'bar'
    Bubble = 'bubble'


class ExtChartUtils:
    @classmethod
    def cleanClass(cls, classObj, retType=dict):

        if classObj is None:
            return []
        variables = vars(classObj)

        if retType is list:
            cleaned = [variables[n] for n in variables if (not n.startswith('_') and not inspect.isfunction(variables[n]))]
        else:
            cleaned = dict([(n, variables[n]) for n in variables if (not n.startswith('_') and not inspect.isfunction(variables[n]))])
        return cleaned


class FunctionsNotAllowedError(Exception):
    def __init__(self, msg=''):

        msg = (
            'Functions are not allowed in datasets. Use an in-line lambda function if necessary, or call the function from outside the chart class\n'
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
