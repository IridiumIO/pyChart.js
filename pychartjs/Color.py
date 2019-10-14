from colorsys import hls_to_rgb, rgb_to_hls, hsv_to_rgb


def RGBA(R: int, G: int, B: int, A=1):
    '''
    Returns RGB(A) Color as formatted rgba string

    Parameters
    ----------
    R, G, B : 0 > 255
    A : 0 > 1
    
    Returns
    -------
    String
    
    e.g Color.RGBA(245, 123, 123, 0.2)
    >>> 'rgba(245, 123, 123, 0.2)'
    '''
    return f'rgba({R}, {G}, {B}, {A})'


def Hex(Hex, internal=False):
    '''
    Takes an inputted hexadecimal value (0x123456) or string '#123456' and
    returns it as a formatted RGBA string
    
    Parameters
    ----------
    Hex : String\n
            "#123456" (RGB) or "#12345678" (RGBA)
        
    Hex : Integer\n
            0x123456FF (RGB) or 0x12345678 (RGBA).
            RGB MUST be padded to 8 long by adding FF to the end
            
    Returns
    ------- 
    String

    >>> 'rgba(103, 58, 183, 1.0)'
    
    '''
    Hex = f'{Hex:08x}' if type(Hex) is int else Hex.lstrip('#')

    if len(Hex) == 6:
        R, G, B = [int(Hex[i: i + 2], 16) for i in (0, 2, 4)]
        A = 1
    if len(Hex) == 8:
        R, G, B, A = [int(Hex[i: i + 2], 16) for i in (0, 2, 4, 6)]
        A = round(A / 255, 3)

    if internal:
        return R, G, B, A

    return f'rgba({R}, {G}, {B}, {A})'


def HSLA(H: float, S: float, L: float, A=1):
    '''
    Returns HSL(A) Color as formatted rgba string

    Parameters
    ----------
    H : Hue 0-360\n  
    S : Saturation 0-100\n
    L : Lightness 0-100\n
    A : Alpha (optional) 0-100
    
    Returns
    -------
    String
    
    e.g Color.HSLA(90, 20, 40)
    >>> 'rgba(100, 120, 80, 1)'

    '''
        
    H, S, L = H / 360.0, S / 100.0, L / 100.0
    R, G, B = tuple(int(i * 255) for i in hls_to_rgb(H, L, S))
    
    return RGBA(R, G, B, A)


def HSVA(H: float, S: float, V: float, A=1):
    '''
    Returns HSV(A) Color as formatted rgba string

    Parameters
    ----------
    H : Hue 0-360\n  
    S : Saturation 0-100\n
    V : Value 0-100\n
    A : Alpha (optional) 0-100
    
    Returns
    -------
    String
    
    e.g Color.HSLA(90, 20, 40)
    >>> 'rgba(100, 120, 80, 1)'

    '''
        
    H, S, V = H / 360.0, S / 100.0, V / 100.0
    R, G, B = tuple(int(i * 255) for i in hsv_to_rgb(H, S, V))
    return RGBA(R, G, B, A)


def Palette(BaseColor, n=5, generator='saturation'):
    '''
    Generates a color palette based on the input
    
    Uses either hue, lightness, saturation or alpha as generators.
    
    Parameters
    ----------
    BaseColor : string of format "rgba(R, G, B, A)" or any Color\n
        
        Use Color.RGBA() or Color.Hex() to convert automatically, e.g:
            >>> Color.Palette(Color.Hex("#2A2A2A"))
        Can also use the built-in colors, e.g.
            >>> Color.Palette(Color.Red)
        
    n : int, optional\n
        
        Number of colors to generate, by default 5
        
    generator : str, optional\n
        
        Method to use to generate colors, by default 'saturation'.
        Options are: 'hue', 'lightness', 'saturation', or 'alpha'
    
    Returns
    -------
    list
        containing all colors in chart-ready format.
    '''

    BaseColor = BaseColor.lstrip("rgba")
    R, G, B, A = tuple(map(float, BaseColor[1:-1].split(',')))
    R, G, B, A = R / 255.0, G / 255.0, B / 255.0, A

    H, L, S = rgb_to_hls(R, G, B)
    H, L, S = H * 100, L * 100, S * 100

    # I'm sorry...
    step = [i for i in range(101)[:: int(100 / (n + 1))]][1:-1]

    LS = []
    for i in step:
        if generator == 'hue':
            R, G, B = hls_to_rgb(i / 100, L / 100, S / 100)

        elif generator == 'lightness':
            R, G, B = hls_to_rgb(H / 100, i / 100, S / 100)
        elif generator == 'saturation':
            R, G, B = hls_to_rgb(H / 100, L / 100, i / 100)
        elif generator == 'alpha':
            R, G, B = hls_to_rgb(H / 100, L / 100, S / 100)
            A = round(i / 100, 3)
        R, G, B = int(R * 255), int(G * 255), int(B * 255)
        LS.append(f'rgba({R}, {G}, {B}, {A})')

    return LS


class JSLinearGradient: 
    '''
    Generates a Javascript function that creates a Linear CanvasGradient object when
    used in HTML/JS
    - Usable within pyChart.JS chart objects

    Returns
    -------
    string (pyChart.JS escaped)\n
            Javascript function generator of the form "<<function(){...}()>>"
    '''
    
    
    def __init__(self, chartContextName="ctx", x1=0, y1=0, x2=1000, y2=0, *colorstops: tuple):
        '''
        Initialises the LinearGradient Object
        
        Parameters
        ----------
        chartContextName : str, optional\n
            name of the Canvas ChartContext to use, by default "ctx"
        x1, y1, x2, y2: int\n
            Coordinates to render the gradient through. 
        
        *colorstops: tuples, optional\n
        
            any number of color stops in the form (stopPosition, Color)\n
                
                - stopPosition must be a decimal 0 <= 1 
        '''
        
        
        self.ctx = chartContextName
        self.coordinates = x1, y1, x2, y2
        self.gradientType = 'createLinearGradient'
        self.ColorStops = []
        
        for stop in colorstops:
            self.addColorStop(stop[0], stop[1])
        
        
        
    def addColorStop(self, stop: float, color: str):
        '''
        adds a Color Stop to the JSGradient Object
        
        Parameters
        ----------
        stop : float\n
            Value 0<=1\n
        color : str\n
            Color to use, either as a pyChart.js Color() object or a string.
        '''
        
        self.ColorStops.append((stop, color))
    
    
    
    def returnGradient(self):
        JSOPEN = "<<(function(){ "
        JSCLOSE = "return gradient})()>>"
        VARGRADIENT = f'var gradient = {self.ctx}.{self.gradientType}{self.coordinates}; '
        
        ret = JSOPEN + VARGRADIENT
        
        for clr in self.ColorStops:
            ret += f"gradient.addColorStop({clr[0]}, '{clr[1]}'); "
        
        ret += JSCLOSE   
        return ret
    
    
    
    def __repr__(self):
        return self.returnGradient()


class JSRadialGradient(JSLinearGradient):
    '''
    Generates a Javascript function that creates a Radial CanvasGradient object when
    used in HTML/JS
    - Usable within pyChart.JS chart objects

    Returns
    -------
    string (pyChart.JS escaped)\n
            Javascript function generator of the form "<<function(){...}()>>"
    '''
    
    def __init__(self, chartContextName='ctx', x1=0, y1=0, r1=0, x2=1000, y2=0, r2=0, *colorstops):
        '''
        Initialises the RadialGradient Object
        
        Parameters
        ----------
        chartContextName : str, optional\n
            name of the Canvas ChartContext to use, by default "ctx"
        x1, y1, r1, x2, y2, r2: int\n
            Coordinates and radii of two circles to render the gradient through. 
        
        *colorstops: tuples, optional\n
        
            any number of color stops in the form (stopPosition, Color)\n
                
                - stopPosition must be a decimal 0 <= 1 
        '''

        self.ctx = chartContextName
        self.coordinates = x1, y1, r1, x2, y2, r2
        self.gradientType = 'createRadialGradient'
        self.ColorStops = [] 
        for stop in colorstops:
            self.addColorStop(stop[0], stop[1])
        
       
#Colors below thanks to Sasha Trubetskoy: 
# https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/

Red         = Hex(0xE6194BFF)
Green       = Hex(0x3CB44BFF)
Yellow      = Hex(0xFFE119FF)
Blue        = Hex(0x4363D8FF)
Orange      = Hex(0xF58231FF)
Purple      = Hex(0x911EB4FF)
Cyan        = Hex(0x42D4F4FF)
Magenta     = Hex(0xF032E6FF)
Lime        = Hex(0xBFEF45FF)
Pink        = Hex(0xFABEBEFF)
Teal        = Hex(0x469990FF)
Lavender    = Hex(0xE6BEFFFF)
Brown       = Hex(0x9A6324FF)
Beige       = Hex(0xFFFAC8FF)
Maroon      = Hex(0x800000FF)
Mint        = Hex(0xAAFFC3FF)
Olive       = Hex(0x808000FF)
Apricot     = Hex(0xFFD8B1FF)
Navy        = Hex(0x000075FF)
Gray        = Hex(0xA9A9A9FF)
White       = Hex(0xFFFFFFFF)
Black       = Hex(0x000000FF)
Transparent = Hex(0x00000000)
