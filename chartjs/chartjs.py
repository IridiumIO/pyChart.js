import inspect
import json
from chartjs.builderutils import ExtChartUtils, FunctionsNotAllowedError

class BaseChart:
  
    class labels:
        pass
    
    class datasets:
        pass

    class options:
        pass
    
    class pluginOptions:
        pass

    
    def __init__(self, *args, **kwargs):
        self.__impDataSets__ = ExtChartUtils.cleanClass(self.datasets) 
        self.__impOptions__ = ExtChartUtils.cleanClass(self.options) 
        self.__impLabels__ = ExtChartUtils.cleanClass(self.labels, list)
        self.__impPluginOptions__ = ExtChartUtils.cleanClass(self.pluginOptions)
        
        if not self.__impLabels__:
            if hasattr(self.datasets, 'data'):
                varx = len(self.datasets.data)
                for i in range(varx): 
                    self.__impLabels__.append(f'Data{i}')
            elif hasattr(self.datasets.set1, 'data'):
                varx = len(self.datasets.set1.data)
                for i in range(varx): 
                    self.__impLabels__.append(f'Data{i}')

    def getLabels(self):
        return {"labels" : self.__impLabels__}

    def getOptions(self):
        options = self.__impOptions__
        options.update(self.getPluginOptions())
        return {"options" : options}

    def getDatasets(self):

        # TODO:: Add catch for misnamed subsets

        subSets = dict([(x, self.__impDataSets__[x]) for x in self.__impDataSets__ if inspect.isclass(self.__impDataSets__[x]) and x.startswith('set')]) 
        subFunc = [x for x in self.__impDataSets__ if inspect.isfunction(self.__impDataSets__[x])]    
        
        if subFunc: raise FunctionsNotAllowedError()

        content = []
        if not subSets: content.append(self.__impDataSets__)

        for data in subSets: 
            subclass = subSets[data]
            content.append(ExtChartUtils.cleanClass(subclass))

        return {'datasets': content}

    
    def getPluginOptions(self):
        target = self.__impPluginOptions__
        plugins = dict([(x, target[x]) for x in target if inspect.isclass(target[x])])
        otherOptions = dict([(x, target[x]) for x in target if not inspect.isclass(target[x])])

        content = {}
        content.update(otherOptions)
        
        for plugin in plugins: 
            subclass = plugins[plugin]
            content.update({plugin: ExtChartUtils.cleanClass(subclass)})
        
        return({"plugins": content})

    def buildJSON(self):
        datasets = self.getDatasets()
        labels = self.getLabels()
        datastructure = {}
        datastructure.update(labels)
        datastructure.update(datasets)
        
        options = self.getOptions()

        build = {"data": datastructure}
        build.update(options)

        return json.dumps(build)

