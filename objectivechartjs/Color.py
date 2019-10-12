from colorsys import hls_to_rgb, rgb_to_hls


def RGBA(R: int, G: int, B: int, A=1):
    '''
    Returns Color as formatted rgba string

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
        R, G, B = [int(Hex[i : i + 2], 16) for i in (0, 2, 4)]
        A = 1
    if len(Hex) == 8:
        R, G, B, A = [int(Hex[i : i + 2], 16) for i in (0, 2, 4, 6)]
        A = round(A / 255, 3)

    if internal:
        return R, G, B, A

    return f'rgba({R}, {G}, {B}, {A})'


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

#Colors below thanks to Sasha Trubetskoy: 
# https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/


Red      = Hex(0xE6194BFF)
Green    = Hex(0x3CB44BFF)
Yellow   = Hex(0xFFE119FF)
Blue     = Hex(0x4363D8FF)
Orange   = Hex(0xF58231FF)
Purple   = Hex(0x911EB4FF)
Cyan     = Hex(0x42D4F4FF)
Magenta  = Hex(0xF032E6FF)
Lime     = Hex(0xBFEF45FF)
Pink     = Hex(0xFABEBEFF)
Teal     = Hex(0x469990FF)
Lavender = Hex(0xE6BEFFFF)
Brown    = Hex(0x9A6324FF)
Beige    = Hex(0xFFFAC8FF)
Maroon   = Hex(0x800000FF)
Mint     = Hex(0xAAFFC3FF)
Olive    = Hex(0x808000FF)
Apricot  = Hex(0xFFD8B1FF)
Navy     = Hex(0x000075FF)
Gray     = Hex(0xA9A9A9FF)
White    = Hex(0xFFFFFFFF)
Black    = Hex(0x000000FF) 


if __name__ == "__main__":
    Palette(Red, 'h', 5)
