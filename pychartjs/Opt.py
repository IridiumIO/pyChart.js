from pychartjs import utils


class General:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            object.__setattr__(self, key, val)

    def build(self):
        vars = dict((k, v) for (k, v) in self.__dict__.items() if v is not None)
        for k, v in vars.items():
            if isinstance(v, General):
                vars[k] = v.build()
            elif isinstance(v, list):
                vars[k] = utils.ChartUtils.cleanOptionsList(v)
        return vars

    def __repr__(self):
        vars = dict((k, v) for (k, v) in self.__dict__.items() if v is not None)
        for k, v in vars.items():
            if isinstance(v, General):
                vars[k] = v.build()
        return str(vars)


class Title(General):
    def __init__(self, text="My Chart", display=True, position='top', padding=10, **kwargs):

        self.text     = text
        self.display  = display if display is not False else None
        self.position = position if position != 'top' else None
        self.padding  = padding if padding != 10 else None
        
        super().__init__(**kwargs)


class Layout(General):
    def __init__(self, padding=0, **kwargs):   
        self.padding = padding  
        super().__init__(**kwargs)


class Legend_Labels(General):
    def __init__(self, boxWidth=40, padding=10, filter=None, fontSize=12, fontStyle='normal', fontColor='#666', usePointStyle=False,  **kwargs):
        
        self.boxWidth      = boxWidth if boxWidth != 40 else None
        self.padding       = padding if padding != 10 else None
        self.filter        = filter
        self.fontSize      = fontSize if fontSize != 12 else None
        self.fontStyle     = fontStyle if fontStyle != 'normal' else None
        self.fontColor     = fontColor if fontColor != '#666' else None
        self.usePointStyle = usePointStyle if usePointStyle != False else None
        
        super().__init__(**kwargs)


class Legend(General):
    def __init__(self, display=True, position='top', fullWidth=True, reverse=False, labels='default', **kwargs):
        
        self.display   = display if display is not True else None
        self.position  = position if position != 'top' else None
        self.fullWidth = fullWidth if fullWidth is not True else None
        self.reverse   = reverse if reverse is not False else None
        self.labels    = labels if labels != 'default' else None
          
        super().__init__(**kwargs)
