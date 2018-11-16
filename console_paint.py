#!.venv/bin/python3
#-*- coding:utf-8 -*-
"""
Prints * Colorful, Bold, Underline * Text
"""

effects = {
    'bold':'\033[1m',
    'unbold':'\033[21m',
    'underline':'\033[4m',
    'ununderline':'\033[24m',
}

def applyEffect(effect):
    """Applies/Removes special effects to/from texts like bold or underline."""
    def wrap1(func):
        def wrap(**kwargs):
            print(effects[effect], end='', **kwargs)
            return func
        return wrap
    return wrap1

@applyEffect('bold')
def bold():
    pass
@applyEffect('unbold')
def unbold():
    pass
@applyEffect('underline')
def underline():
    pass
@applyEffect('ununderline')
def ununderline():
    pass

class Color:
    def __init__(self, c):
        """Colors can be supplied as dict, tuple, list or string in the format rgb(X,Y,Z) or #XYZ."""
        if type(c) not in [tuple, list, str, dict]:
            raise TypeError(
                'Colors can be initialized from type list, tuple, dict or str.')
        elif type(c) == dict :
            c = c['r'], c['g'], c['b']
        elif type(c) == str  :
            if c.strip().startswith('rgb') :
                c = c.replace(' ', '').strip('rgb()').split(',')
            elif c.strip().startswith('#') and len(c) == 7 :
                c = c.replace(' ', '').strip('#')
                c = '0x'+c[:2],'0x'+c[2:4],'0x'+c[4:]
        c = [int(str(component), 0) for component in c]
        if min(c, key=int) < 0 or max(c, key=int) > 255 :
            raise ValueError('Color values can be in range 0 - 255.')
        if len(c) != 3 :
            raise IndexError('RGB colors require exactly 3 color components.')
        self.rgb = c
    def __iter__(self):
        return iter(self.rgb)
    def __str__(self):
        return 'Color(R:{} G:{} B:{})'.format(*self.rgb)


def painter(*args,
            end='\n',
            color=None,
            background=None,
            isBold=False,
            isUnderlined=False,
            **kwargs):
    """Prints 8-bit RGB Text using ANSI Select Graphic Rendition.
    Color and background can be Color type or anything that Color accepts.
    """
    # check if color is undefined or already a Color object.
    colorify = lambda c: Color(c) if (c and type(c)!=Color) else c
    color = colorify(color)
    background = colorify(background)

    # Applying effects
    if isBold :
        bold(**kwargs)
    if isUnderlined :
        underline(**kwargs)

    # check if color is undefined (like None or '')
    if not color and not background:
        print('\033[49;39;m'.format(), end='', **kwargs)
    elif not color:
        print('\033[39;48;2;{};{};{}m'.format(*background), end='', **kwargs)
    elif not background:
        print('\033[49;38;2;{};{};{}m'.format(*color), end='', **kwargs)
    elif color and background:
        print('\033[38;2;{};{};{};48;2;{};{};{}m'.format(*color,*background), end='', **kwargs)
    # endline always resets
    print(*args, end=end+'\033[0m', **kwargs)


if __name__=='__main__':
    pass
