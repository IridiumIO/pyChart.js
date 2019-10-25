import inspect
import json
from pychartjs.utils import ChartUtils, ChartType, FunctionsNotAllowedError
from pychartjs.Opt import General

class BaseChart:

    type = ChartType.Bar

    class labels:
        pass

    class data:
        pass

    class options:
        pass

    class pluginOptions:
        pass


    def getLabels(self):
        cleanLabels = ChartUtils.cleanClass(self.labels, list)

        if not cleanLabels:
            cleanData = ChartUtils.cleanClass(self.data)
            if 'data' in cleanData.keys():
                for i in range(len(cleanData['data'])):
                    cleanLabels.append(f'Data{i}')

            elif hasattr(cleanData[next(iter(cleanData))], 'data'):
                for i in range(len(cleanData[next(iter(cleanData))].data)):
                    cleanLabels.append(f'Data{i}')
        if len(cleanLabels) == 1: 
            cleanLabels = cleanLabels[0]

        return {'labels': cleanLabels}


    def getOptions(self):

        cleanOptions = ChartUtils.cleanClass(self.options, General)
        cleanOptions.update(self.getPluginOptions())
        return {'options': cleanOptions}


    def getDatasets(self):  # TODO:: Add catch for misnamed subsets

        cleanDatasets = ChartUtils.cleanClass(self.data)

        subSets = dict([(x, cleanDatasets[x]) for x in cleanDatasets if inspect.isclass(cleanDatasets[x])])
        subFunc = [x for x in cleanDatasets if inspect.isfunction(cleanDatasets[x])]

        if subFunc:
            raise FunctionsNotAllowedError()

        content = []
        if not subSets:
            content.append(cleanDatasets)

        for dataSet in subSets:
            subclass = subSets[dataSet]
            if not hasattr(subclass, 'label'):
                subclass.label = dataSet
            content.append(ChartUtils.cleanClass(subclass))

        return {'datasets': content}


    def getPluginOptions(self):
        cleanPluginOptions = ChartUtils.cleanClass(self.pluginOptions)

        target = cleanPluginOptions
        plugins = dict([(x, target[x]) for x in target if inspect.isclass(target[x])])
        otherOptions = dict([(x, target[x]) for x in target if not inspect.isclass(target[x])])

        content = {}
        content.update(otherOptions)

        for plugin in plugins:
            subclass = plugins[plugin]
            content.update({plugin: ChartUtils.cleanClass(subclass)})

        return {'plugins': content}


    def get(self):

        datastructure = {}
        datastructure.update(self.getLabels())
        datastructure.update(self.getDatasets())

        options = self.getOptions()

        build = {'type': self.type}
        build.update({'data': datastructure})
        build.update(options)

        js = json.dumps(build)
        js = js.replace('"<<', '').replace('>>"', '')
        return js
