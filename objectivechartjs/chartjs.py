import inspect
import json
from objectivechartjs.builderutils import ExtChartUtils, ChartType, FunctionsNotAllowedError


class BaseChart:

    type = ChartType.Bar

    class labels:
        pass

    class datasets:
        pass

    class options:
        pass

    class pluginOptions:
        pass


    def getLabels(self):
        cleanLabels = ExtChartUtils.cleanClass(self.labels, list)

        if not cleanLabels:

            if hasattr(self.datasets, 'data'):
                for i in range(len(self.datasets.data)):
                    cleanLabels.append(f'Data{i}')

            elif hasattr(self.datasets.set1, 'data'):
                for i in range(len(self.datasets.set1.data)):
                    cleanLabels.append(f'Data{i}')

        return {'labels': cleanLabels}


    def getOptions(self):

        cleanOptions = ExtChartUtils.cleanClass(self.options)
        cleanOptions.update(self.getPluginOptions())
        return {'options': cleanOptions}


    def getDatasets(self):  # TODO:: Add catch for misnamed subsets

        cleanDatasets = ExtChartUtils.cleanClass(self.datasets)

        subSets = dict([(x, cleanDatasets[x]) for x in cleanDatasets if inspect.isclass(cleanDatasets[x])])
        subFunc = [x for x in cleanDatasets if inspect.isfunction(cleanDatasets[x])]

        if subFunc:
            raise FunctionsNotAllowedError()

        content = []
        if not subSets:
            content.append(cleanDatasets)

        for data in subSets:
            subclass = subSets[data]
            if not hasattr(subclass, 'label'):
                subclass.label = data
            content.append(ExtChartUtils.cleanClass(subclass))

        return {'datasets': content}


    def getPluginOptions(self):
        cleanPluginOptions = ExtChartUtils.cleanClass(self.pluginOptions)

        target = cleanPluginOptions
        plugins = dict([(x, target[x]) for x in target if inspect.isclass(target[x])])
        otherOptions = dict([(x, target[x]) for x in target if not inspect.isclass(target[x])])

        content = {}
        content.update(otherOptions)

        for plugin in plugins:
            subclass = plugins[plugin]
            content.update({plugin: ExtChartUtils.cleanClass(subclass)})

        return {'plugins': content}


    def get(self):

        datastructure = {}
        datastructure.update(self.getLabels())
        datastructure.update(self.getDatasets())

        options = self.getOptions()

        if type(self.type) is not str:
            self.type = self.type.value

        build = {'type': self.type}
        build.update({'data': datastructure})
        build.update(options)

        return json.dumps(build)

