"""
   sprites.py

   一、简介：
   
       本模块叫精灵模块，主要提供继承自Turtle的Sprite类与AnimatedSprite类。并且重定义了Turtle模块中的一些方法和属性。
   由于要旋转图形，所以需要PIL模块支持。默认的精灵对象是抬笔的，内置14张图片。 分别是：ball.png，bug.png，
   b1.png,b2.png,cat1.png，cat2.png，cat1_l.png，cat2_l.png，explosion0.png,explosion1.png，fighter.png，
   thunder.png，sky.png，ufo.png。它们存在于_built_in_images列表中。在本模块第一次运行后，这些图片会释放
   到当前工作目录的res文件夹。本模块设计为教育目的，可用来做启蒙型的动画与小游戏。
 
   二、Sprite类主要提供了以下功能：
   
   1、角色可直接拖动(compound造型不支持)。
   2、提供像Scratch中的三种旋转模式。精灵对象的_rotatemode属性值为0，代表可360度旋转,为1时代表可左右翻转,为2时角色不会旋转。
   3、rotatemode：返回或设置旋转模式。   
   4、addx：x坐标增加。
   5、addy：y坐标增加。
   6、scale：缩放，只有一个参数。
   7、gotorandom：到随机位置。
   8、heading：重定义了这个方法，不带参数能获取当前朝向。带参数参让角色朝向某对象或坐标。
   9、show：显示对象。
   10、hide：隐藏对象。
   11、mouse_pos：获取鼠标指针坐标。
   12、move：移动水平dx距离和垂直dy距离。
   13、collide：和另一个角色或图章的碰撞方法，采用的是矩形碰撞。
   14、collidemouse：碰到鼠标指针
   15、collide_edge：碰到边缘检测
   16、bounce_on_edge：碰到边缘就反弹，适合于用fd命令让角色前进后再使用。
   17、bbox：获取角色绑定盒，也可获取图章的绑定盒。
   18、randomcolor：随机颜色，较鲜艳。
   19、randomheading：随机方向。
   20、remove：移除方法,把自己从屏幕的_turtles列表中删除，并根据item号删除自己在画布上的形状，清除说话泡泡对象。
   21、stampmove：根据图章编号水平和垂直移动图章。
   22、stampgoto：移动图章编号到指定坐标，暂不支持复合图形的图章，它们的图章编号是一个元组。
   23、say：说话方法，会显示气泡。默认时间为2秒，默认阻塞进程。
   24、saycolor：返回或设置说话的字的颜色。
   25、saybordercolor：返回或设置说话泡泡的边框颜色。   
   26、write：重定义写方法，增加angle参数，可以写斜字，默认为黑体，12号。

   三、AnimatedSprite类：
   
   本类继承自Sprite类，主要提供对造型的管理。在实例化时，需要传递给它向右序列造型和向左序列造型。

   四、screen新增命令：
   
   1、resizable：默认窗口是不可变大小的，用这个命令能让窗口重新可缩放。
   2、onmousemove：即鼠标移动事件。
   3、onscreenrelease：鼠标松开事件。
   
   五、单独函数：

   1、makecolors：
   默认产生128种鲜艳的颜色，导入本模块后它会运行一次，产生一个_colorlist列表。

   2、mouse_pos：
   获取鼠标指针的坐标，和屏幕的xscale和yscale无关。

   3、explode：
   产生爆炸效果的函数。需要传递坐标和序列帧图。

   六、单独类：
   
   1、Key类：用来新建某个按键的实例，用于在循环中进行键盘按键检测。
   2、Mouse类：用来新建鼠标按键的实例，用于在循环中进行鼠标按键检测。
   3、Clock：用来固定帧的时钟类，有tick方法和getfps方法。前者用来设置帧率，后者获取帧率。

   七、其它：
   新增屏幕的_focus属性，用来跟踪屏幕是否激活。
   
   注意以下问题：
   1、不支持复合图形的拖动。
   2、不支持复合图形所盖的章的直接坐标定位，但是可以相对移动。
   3、tilt倾斜等变形命令不会对图形进行变形。

   如果用屏幕的tracer(0,0)关闭了自动刷新,那么在移动角色后要马上刷新屏幕,否则会出现意外。
   (目前估计原因可能是绑定盒命令不能及时获取角色最新坐标所致。)
   本模块已经把屏幕的自动绘画延时设为0了。

   其实Turtle模块可以支持png图片,但要像以下这样写:
   screen.addshape('scratch.png',Shape("image", screen._image('scratch.png')))
"""

__author__ = 'lixingqiu'
__date__ = '2019/12/8'
__blog__ = 'www.lixingqiu.com'

try:
  from PIL import ImageTk, ImageOps,Image
except:
    print("本模块需要pillow模块支持，请先在命令提示符里安装。")
    print("命令形式为：pip install pillow --user")
    print("如需帮助请email to ：406273900@qq.com")    
    import sys
    sys.exit()
    
import os
import time
import base64
import random
import colorsys
from io import BytesIO
from copy import deepcopy
from turtle import TK,_Root,_CFG ,TNavigator,Tbuffer,TPen,_Screen,Screen,Turtle,Vec2D, RawTurtle,TurtleScreenBase,Shape,TurtleScreen,_TurtleImage,TurtleGraphicsError 

_CFG['delay'] = 0
# 定义资源文件夹
_resfld = os.path.join(os.getcwd(),'res')
if not os.path.exists(_resfld):os.mkdir(_resfld)

# 重定义Tpen类的_reset方法,让精灵实例化时不落笔
def TPen_reset(self, pencolor=_CFG["pencolor"],
                 fillcolor=_CFG["fillcolor"]):
    self._pensize = 1
    self._shown = True
    self._pencolor = pencolor
    self._fillcolor = fillcolor
    self._drawing = False
    self._speed = 3
    self._stretchfactor = (1., 1.)
    self._shearfactor = 0.
    self._tilt = 0.
    self._shapetrafo = (1., 0., 0., 1.)
    self._outlinewidth = 1
TPen._reset = TPen_reset

# 重定义_Root类的初始化方法
def _Rootinit(self):
    TK.Tk.__init__(self)
    self.resizable(0,0)
    
_Root.__init__ = _Rootinit  

# 重定义原生海龟的初始化方法
def RawTurtle__init__(self, canvas=None,
             shape=_CFG["shape"],
             undobuffersize=_CFG["undobuffersize"],
             visible=_CFG["visible"]):
    if isinstance(canvas, _Screen):
        self.screen = canvas
    elif isinstance(canvas, TurtleScreen):
        if canvas not in RawTurtle.screens:
            RawTurtle.screens.append(canvas)
        self.screen = canvas
    elif isinstance(canvas, (ScrolledCanvas, Canvas)):
        for screen in RawTurtle.screens:
            if screen.cv == canvas:
                self.screen = screen
                break
        else:
            self.screen = TurtleScreen(canvas)
            RawTurtle.screens.append(self.screen)
    else:
        raise TurtleGraphicsError("bad canvas argument %s" % canvas)

    screen = self.screen
    TNavigator.__init__(self, screen.mode())
    TPen.__init__(self)
    screen._turtles.append(self)
    self.drawingLineItem = screen._createline()
    self.turtle = _TurtleImage(screen, shape)
    self._poly = None
    self._creatingPoly = False
    self._fillitem = self._fillpath = None
    self._shown = visible
    self._hidden_from_screen = False
    self.currentLineItem = screen._createline()
    self.currentLine = [self._position]
    self.items = [self.currentLineItem]
    self.stampItems = []
    self._undobuffersize = undobuffersize
    self.undobuffer = Tbuffer(undobuffersize)
    self.tag = 'turtle'                   # 贴一个标签
    self._update()
RawTurtle.__init__ = RawTurtle__init__

# 给原生海龟对象增加move方法
def _move(self,dx,dy):
    """移动水平dx,垂直dy的距离"""
    x = self.xcor() + dx
    y = self.ycor() + dy
    self.goto(x,y)
    self._update()
RawTurtle.move = _move

def __write(self, pos, txt, align, font, pencolor,angle):
    """
       用指定的颜色和字体在画布上写文本。返回文本项目和其绑定盒的右x-1坐标。
    """
    x, y = pos
    x = x * self.xscale
    y = y * self.yscale
    anchor = {"left":"sw", "center":"s", "right":"se" }
    item = self.cv.create_text(x-1, -y, text=txt, anchor=anchor[align],
                               fill= pencolor, font=font,angle=angle)
    x0, y0, x1, y1 = self.cv.bbox(item)
    self.cv.update()
    return item, x1-1

TurtleScreenBase._write = __write

def _write(self,txt,align,font,angle=0):
    """海龟的write的预定义方法
    """
    item, end = self.screen._write(self._position, txt,
                                   align, font,self._pencolor,angle)
    self.items.append(item)
    if self.undobuffer:
        self.undobuffer.push(("wri", item))
    return item,end                 # 本来只返回end,这里增加了item

def _writea(self, arg, move=False, align="left", font=("黑体",12,"normal"),angle=0):
    """在海龟的当前坐标写文本。
    参数:
    arg -- 要写在海龟画图屏幕上的信息,
    move (可选) -- True/False,
    align (可选) -- 左，中，右( "left", "center" or right"),
    font (可选) -- 三元组 (字体名称, 字体大小,字体类型),
    angle (可选) -- 角度值,如90,180

    根据对齐方式和给定的字体样式在屏幕写文本。
    如果move为真，那么海龟(画笔)会移到文本的右下角，缺省为假。

    举例 (假设有一个海龟实例为turtle):
    >>> turtle.write('风火轮编程 ', True, align="center")
    >>> turtle.write((0,0), True)
    """
    if self.undobuffer:
        self.undobuffer.push(["seq"])
        self.undobuffer.cumulate = True
    item,end = self._write(str(arg), align.lower(), font,angle)
    if move:
        x, y = self.pos()
        self.setpos(end, y)
    if self.undobuffer:
        self.undobuffer.cumulate = False
    return item                   # 这里本来不返回item

RawTurtle._write = _write         # 重定义_write
RawTurtle.write = _writea         # 重定义write

# 重定义TurtleScreen的监听
def TurtleScreen_listen(self, xdummy=None, ydummy=None):
        """为了收集按键事件而在海龟屏幕上设置焦点。
        """
        self._focus = True
        self._listen()
TurtleScreen.listen = TurtleScreen_listen
        
def _Screen__init__(self):
      """新建一个窗口,如果存则,什么也不干"""
      if _Screen._root is None:
          _Screen._root = self._root = _Root()
          self._root.title(_Screen._title)
          self._root.ondestroy(self._destroy)
      if _Screen._canvas is None:
          width = _CFG["width"]
          height = _CFG["height"]
          canvwidth = _CFG["canvwidth"]
          canvheight = _CFG["canvheight"]
          leftright = _CFG["leftright"]
          topbottom = _CFG["topbottom"]
          self._root.setupcanvas(width, height, canvwidth, canvheight)
          _Screen._canvas = self._root._getcanvas()
          TurtleScreen.__init__(self, _Screen._canvas)
          self.setup(width, height, leftright, topbottom)

      self._focus = True          # 描述窗口是否失去焦点的逻辑属性
      self._root.bind("<FocusIn>", self.got_focus)
      self._root.bind("<FocusOut>", self.lost_focus)
      
def _got_focus(self, event):
    """得到焦点而发生的事件"""
    #self.cv.config(background="red")
    self._focus = True

def _lost_focus(self, event):
    """失去焦点而发生的事件"""
    #self.cv.config(background="grey")
    self._focus = False
        
_Screen.__init__ =  _Screen__init__  
_Screen.got_focus = _got_focus
_Screen.lost_focus = _lost_focus
_Screen._title = 'Python Sprites Module' # 默认标题

@staticmethod
def _image(filename):
    return ImageTk.PhotoImage(file=filename)

TurtleScreenBase._image = _image

# 重定义TurtleScreen类里面的register_shape方法
# 目的是让它支持png等图片
def _register_shape(self, name, shape=None):
    if shape is None:
        shape = Shape("image", self._image(name))
    elif isinstance(shape, tuple):
        shape = Shape("polygon", shape)
    self._shapes[name] = shape

TurtleScreen.register_shape = _register_shape
TurtleScreen.addshape = _register_shape

# 让窗口可以支持自定义缩放,默认是不支持的
def _resizable(self,width=True,height=True):
        self._root.resizable(width,height)

TurtleScreen.resizable = _resizable

# 重定义Shape类的初始化方法
def _shape__init__(self, type_, data=None):
    self._type = type_

    if type_ == "polygon":
        if isinstance(data, list):
            data = tuple(data)
    elif type_ == "image":
        if isinstance(data, str):
            if isfile(data):
                data = TurtleScreen._image(data) 
    elif type_ == "compound":
        data = []
    else:
        raise TurtleGraphicsError("无此形状 %s" % type_)

    self._data = data

Shape.__init__ = _shape__init__

if not os.path.isfile(os.path.join(_resfld,'explosion0.png')):
    __explosion0 = b'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'
    __explosion0 = BytesIO(base64.b64decode(__explosion0))
    __explosion0 = Image.open(__explosion0)
    __explosion0.save(os.path.join(_resfld,'explosion0.png'))
    __explosion0.close()

if not os.path.isfile(os.path.join(_resfld,'explosion1.png')):
    __explosion1 = b'iVBORw0KGgoAAAANSUhEUgAAAE0AAABOCAYAAABlnZseAAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6AAAdTAAAOpgAAA6lwAAF2+XqZnUAAAp90lEQVR4nGJhGFjAiET/h7L/41BLrFnIgFyz8AKAAGKhhaFEAEYoZmJA9SzIk/+gNCkeRjfvPxZMNQAQQAMRaDAPMoMwkMEM9BEjkP7/HxJgIPyXARF4yPrQUyNyYIHMYwJymP4jAv8PlGZgoGLAAQQQvQMNOcBYgAxWLgYGNgZI4IE89fcbA8NvIOPPf0jA/UXTh556QIEFCigWqHnMnED8HSj3DxJgIPk/UHOoluoAAoiegYaSKkABxs3AwM4OxKwQT4Mk/wP5v38yMPz6Bgk4kIf/w/ShpUSQIMgsNmDAs4ICjhWaeoE0w2+gGcDAYwYq/gXhwvWip2CSAUAA0SvQULIkELMBA4yDh4GBE5gy2JmhgQYCHNDUBkx+vxkhgQZOYSBf/oLQf79Dsx0nNLWyQgOeFRJIIPP/A/WzgjBQDytQ/c//0BTMQIUsCxCAtzJaARCEAaBEUvj//5qwzTrbBr360oM4FAc7b/oHtASWLXQ0h9YAdE5os7g7PgQUGqwrxSqxxlv3ghPPZ5w19kckrQke7XbmDSJmPoRYsPfC3s5l9KD0NbiUxbZ9BBCtAw05hbGBUhYIc0ACjBuUrZgg2QnsDlDg/IVmH6Cv/jJBs+E/SNZk/AUJiH/QAPkD9QATKKWBzGGD2AOyEKTmHzCQ/4CyKVAN8xdoZfMVag8Dahn3D4kmCAAC0FoGOwCCMAwdUzSSEP3/X3UZrukS9eBRLhxgbLyMlr+gPf9fyFEDVjtE9i7SG6FtC7tCJ1Y7NC9mjLNKzQI5OKwGAMcTi3WD7hXGKIDlrGkoOM8j3mPvvLLDPV21pF76uGGdTPNy6M9xCUBr2esACMJA+FBDWPyJvv+DEip4l3ZwdHFpSFMofLmW/gHtrS49QsDKTmAncG3AwfWqsoLfsNvMUrt95JgCuCAyIPGQLJ/gxhwi9VRCq4InOD2AweNlBunLP5phaa5SY+7EPbl4j+s1+mfI6/Pv+gjAarnkAAjCULBKQfbo/U8pGsLHvtbo1oVsIU0zDH38De2BRZZoSMiYBJhYljaiFeBgmxzwFVbNVNoijTtqrqpGXf4LAxVCJ+amCYtas2z301IxB0dHMXD9Bjcc29NTcycBN+RCqjbDsNvb7MSMi4CfDR7tb+B8WpcAtJZLDoUgEAQbg6KJiQuNev9Dqvh9NfAu4EJ2EALpmmboT6AVOQY01uxxWQukbpCmUZoB19deje15EAaweLe4p0R4oYN3d/NYLmznfKRPbUC7UpYzZSZ0Y1Ltj8LitAIxpoYfgF7l2JJK5pOFnC2EUzXwylwTcZUOztntJ/7HllfjJwDr5bLCIAxE0UnGJIpYKBWh//+FRVFpNfZM7KLbQhfZZ07uY/J3aFzCASyhrA47XLrTjrc70AA3XFV6vNlizlDUAVXfoCBFNbXsufHbayeKzFMjdCap9QHgjfDPsloTooyFoSOvE4LK+FQKJLGRRArgK03ZQzw7iMszYI4SAeUHYsdUzvBV/OTg8UN7vgVgvQpyEIZhWJKmVWGTEExD+//3ODANIagg65yNCxdO9Nyqjhs77t9JqxsoN9/shA0gCvI890IDiDwdmLpWqIEJ5aQUckNaj2GWPaZdZHtEKfY0jtWStCjmsuYPtjsVkDUB8LhmMkHyV/JzLu33nJDRFI+Ai7133OwY5qU7kHYFrhuxFExh22SILa/w/ZXzjrOf1X3WIgDrZZeDMAgE4YUFWmyKGn/uf0NtIykt4jotifHFN7nBzg7fzvxLtE/a15VjDtnJrxyB244Q7gSWnSHYZccUglBohXzf44petXMHYxXuG06hPEUV27HvREKelzzE1y2Ce/iT07jQfRRqH5oGbTAkWDg1lOBW5j3mb4oSy5tjTO0NqrgiOpGycFs2W+MwqVBZ4wk0tXPlHce68O+69vO9BWC9jFYQBsEofPx1zXKbm0Q3vf+7RRC7yUEtpWOOrrsIxDsRDn7n//xHaN+vETc7Vg9zDM2RvKF02iAIgYGNBieiOfUt3OTR+bMaumDMflegFk4AU3nypJyHEBuT74u9XRO4Yp+oKxmHWXBh6Ss2+sO2iM+jbl4ea1I6CdPPRet0qq6yMLiZFcl2K25TguF1wgmiN8f7kLG9NMEPE/QtAOlls4MwCARhFtCkWqrRYkzw/Z/PXtRo4/qxYuLFk4e9LmEY5udf0D4H1TRedayKvulYZRhaNuy8yzCr5ODKKO44rtz+UKTrT15kw4Dwu5ojQHNq6yYDsU5YLiSD1HDRflK3hsXJGoBYar09t9w/+Tt40x4ibtw9gFxVr3gvi6FWSDzsmRKvFuwER7EgjC7GpmuxfdH5iwg/gXsJQIq5rCAMA1F0JiqtjxAqiiCKLnTp//+RO3GptW3imZTsBRfZJuTOzZk7+Ue04rA8GiHY0gRr4BbA3+wAP/A/sM5HJ9dLJad9LX61VnU3jt1ORgRbX4Tk0iHHh7q/ZRyUnlzpNWT/6lylXiTrgtp0Eu7KBEAW6732KdA8Zimqc0SMyrVpioLEMqKwWnRh6+hhXRg0PhCuzV8gVhIzXmFZMcBPz/MrACtmzIJADEPhpGlLPRRxcLhBbzlU8P//LoVTkOOkfuHERUcLHTK0Ca/Jy0v/AZrLC58hly5gIf0tHNayd53K4ShyPhXp27VG23AEBKUDHOegTGwLQhhJt2ucxYNPjw6i2w8H7flRfXQHyZh7/DVB+rzSlIqaKXeTNFHS5RZ0CLzjKIWJ4Q6aVsnmqg3cRqkaTWV6Q4IXdY4b5hLV+v0p+nO9BODEWlYYhIHg7qZ5IEi9eKkIIij0//+tQomxs4lSj+ItJMuSLDPMTO4O7WicI4wvg6uAj6cOTlHWE40D0XuyNL1qNtLhijOqO02Kj2IzG7RplIbYA3czsiLOFm2P9Rds+Wz560NpljPEUoJoC4F1JKNHdHUswXEIhqwXQE4NhLCFrZAovCbYlQQ1TQi5Wzw9wuxoc38xkCti8BNA5AYaeAAQ2iYDeRlULrABsycnMHsKABuwkrKMDIoqjAwKMsCajUkMqFwKiMWhgzhf/0I6TCKskH6BANC5PKBAA1Z5r0ADOQzgFikDByOkd/gOiD8xoAxJgpKLALBG1BJilONiYOLhYfjLz8H4i4f9Hyuw2/UX2EH/++UvsKf0h+n/n3///v4F9p9+fweZBux5gEIL1PSAdb1YoTUp0hjeP3wBBxCANPNrQRCGovi2JClNqMiC8M3v/818KdvA1NvvOkl86KnB2Ab7wx333p1z9o+n2Vk6dVlUYFMl5UCL05WEf7PmXqVmN+Gm3ER6/BxjyB1ZlXP0i1qyVcktXWi9vmOQo8DcA/0C6wI2NIwfsv4FUIQ1EK6krjqRs1K1vX2DaCao67YgvCDih166Dl/jZA++GIHNKin1G/OlXC6ZlWTscO3ibT/LRwBSzKAHQRiGwt0AcZGFELiYeNSL//9/GRMHQ2DzPXvg5sVDkyVNlu5b1+71r5pmtGVzCHg86EDRd9SYVs4XgEO5MgKaX2PV4CzBIaQBJG9esbeA5OE4wd9ghw0AqSo5+Qqw2mgWdlgjFeQhmomMnIrziUe4WOldLu91eWVXsvhzuGWrwju9YsphGlMEjUJAZJ0kUWFFvUYKiFzoOcy8/wZ+QvsIwIkZ9CAIw1C4Dk2cMUCIHuTsyf//jzxjBBJDYKBfV+DIwUMPy5qte+323voPaEu+YweDBTwQeJUY2DXdSXmjysqE+TUEZ56qx0hnbA4h3KTg0Dmhn5Tw94ZuivHvkZciRJUpeVzc3OnCl++EKhJpR+vFcgkjuLBrdv4mj6O7H9AvzyH4dz9WYNp8Kmq6kXqCUwEmdPYQTL2lSMfBSFXmTbbZ8yeASA00eDMD1OHmhzQzQH1LERFIE0NaAoSZGMSBJSwklYGyJzABMQALOgZgMmQAtnAZOEAFPtAEgX+QAGEEOQNa2vMA450bSAsA064ssKx78AMcIAwv/0Mqi9dA+RdApY/+Q1LaX1B6+QcpjYBlJTfbf2ZNlv8KwLYx94v/DK8+vmd4//4Tw3u2XwwvQSOTwHLt+xdIQQHS/Qs6UgKal/gNndRBnoTBCgACiJRAQ54UgTVkBYBliQho9EIK2CaTAxb8CowMsuLAhj2ohgCXU8B8ygDMrwzA0GSQBXpYFlRjAp0uC3SuMDt0CJIN6hQWSCkDwqAyjfcPJLBFge6/AeRf+wsZdgSNTwDbCWAMSh6gmhgkBsq238B1CJMiM4MYsLgUff+R4fPznwzPgFUpGyhggPXJxzcMDG/+QeYafoGGwX9DhsLB8wgMiOlDnAAggMgJNPCwDw+kTSYhDawXVRgYVDQYGbS1WRi0NFkZxMEtcJCn+UGFPDAAxIDagF0DBmD7g0EJyBcGeRTktt9IToBNXbJC+UAvgWoQUCdSAZjaPgPNeg5U8+4/JMWC1AI7oQxfgPJf/kMCDqTlK0QrI7B25AFi7l/g0WJuUCsEGDBfgRXxazboWB4owD5BRky+QwMMNmuFN3sCBBCp2RPUv2QHjZMBHSIE6oQDG5pKmgwMOjoMDHpawPKME9gbAiec/9ApYFDgyQB1ybFAAg5UI7LC5jRYkQILVsPDymFQyICSzg9IZ0eXAVKvsQG9ew9ICzNDpN8D2W+AYh/+QYp2UHn3C2rUX4hJwFzBAoxY5Q//Gb48Y2B4xgopNEAh9Pc7IoX9IibAQAAggEhOaaDJWFjzAlSOgbKlMtBB2owMkhywLsl/qMm8kI44eLQeNKEGmmcCTbSBjfrBgGg7gMRANQQotEH9T1Ab5QtUngviexZgCGn/gXgLVBZ+AMq9YYCUd8AaiOHtH8h0yhdoWP9iQHS/gcLACGZRZGBQfAosJR8CMTDwnrJC/AJq1MJmvGD+hPkCKwAIIJJrT0bo8A8XZKJEEBhwEvLADMQB8j0sDGCJCOR/2Lw3ByioOSABCI5oWKAgO4UbqokL6mtWaABCW7WgUTp9oFmKQP4FYCBxgso8SOnO8BLajwUFHMgNoMbwNwb4HBOodaMEDO5XDAzqwIB7/hzYjAZm1Y+gsuwbpDqBxSJyasMacAABRGygwaf/QV0ODkgzAzwyC0ptwMYsO6pKqD9BiZ4f6AY+oOe4gT7hZIZ0ocC+44YGCshd36E0OwNiPpkfKv+OAbEs4w8krfMDDdf8D6kgvn+HzJC+ANL8fyCu5AeKPwIqfwLVygShWYDlGjDg1B8Dg/glEAPrkU+/ITXmv4+Q1AarPbGtJYEDgAAiFGjIM0ss0NYUuJ8J9JIAMMAkgalMDtiXZoIHGMxK2AgGKNEAS2MGIWBESrBCyjkwYIUGHqzX8h/KZoHyf0GtZoMGKgsDfEYQ1EQR+wcJNJAeUI36A8h/9AdiDGieHdQHACXmN6gBJ/6fgVUDWAa/gbQEv/6GWs4IadyCouDXP0T5hrUrBRBA+AINeegHPPzDD+mU8wIzjDCwUy4FDDAleUZgMxVWhsFmEEGAHSoG8oASEMuB2tuwpgU7NDT/QAMH1m0AZUVQCgRVAqD2xEeogaC8xgFVzwrBoMk40MQcA3RADpSSgaEB7l0c/AaZb/oB1fIJagwjZNAEqEwMWCnoAsP0w3dIjIBSGMMHoIVAJV+hZRzyAhwUABBAhAIN1CYDNzFA3SQByHiZiASkHFMG1khqvKCAhfcRGBAJiA8aBsD8wKD5Dzr+DMKgRPsNyQqQIl5oYIHaIopQZ72G+vgjktthJTuIFmJAJIhfEHWg2JMC6tX7C+mGgZojH/5jLH8BBjOj4n8GBWAb+QlQ11vQlOBv6Oz9Z0Rg/WZAnX2HA4AAwhVoyKmMjR2SygSAgSYKbGtKA1v+SsAaU1WTkYEfnC9BAQVKKBxQDAowWSA2AmJVRsSaILAifgZEMwPEF4AaAOo2AJvJDJLQQAAFLKhl+xXK/gn1B2xwh48Bkax/IQKWCRgEksBYkwaqUwbquccASbSwBVfMkAQKbAWxS/1jkAfWok+A3dl3oKYHKNWBAo8LMlX4B2mGCiXgAAIIX6CBUxkfpCHLJwBp/UuCW/5ADGzUyoGbGMzQgAJFPCzBKAMDxQOIA5ggS1MY2aCBJQr1LDdUEyc00EB8UJYVhhryE6oW5E4RaACDeuqfGBDlHiwSmKGBxwQ1DxgMQkD7tP5BZjkf/YWEOSvU69BeA2juANgrExH+yyAGdNkroC0fgYH2BRiev/9AY+cbJJv+Qg84gADCFmiwAAM1Kzi4IYU+nwgzg5QiG4OK3D8GOck/DJLARr4APDtyQ90PmjcHdZusgYKObJDaEp4qxKCBAgpASSgbFPUSSOKCDIhaVIABUYlB22rgVAedCQaLs0HV/kAK+LeQVR8yoKlhoPyLn5BGMbCdAa6IP0Lii5H5P4PEVwY+0BTjy78MIqDy7RukLwqqCED1MSjl/fuPpVsFEEBYAw3UFoMFGGg0VgDYh1PgZlLWF2TSk/nLKMP77rcAP7BVBk5ATFD3glr7oNFZLVDrnxEywAj2BEiSBxoIoFQESnHiUD7ILUrQFMIJFUduasDKr/9QeW5oAMECjgkacEKQ5AOuLkHsP5BFDPJANRb/IcPqD4H41T9IbfocyH7wj4Hv539GYOuEFzQW9+k/g+C3fwxfgaZ/BQbzN2CAcYC6WV+xzMADBCDTSlIAhGGgpai4ohdFf+D/P+ZBQdxqxkxF9BDaQwhlmIR0ki9oD8sw7I11DFeUTuqZMKuJjNDZtUV4iztG01K8ewGrsyoo4nNeeeWiJAg+BSuyDPftBWhP851xQAAnArMQHNhIv3dtTuhjGY+1z8o5xLq0BXEzWbXHQ0jM8ObTZIfL5FVpvQc59ONJW3Dsjvjm6Kd4XAIIOdDAhT+oVgYt6+SElGWgNWQgzPHv278/n94yfhRi+Pdd/B+wG84BVA8KEwNgqjDjgHSZfvyBZE95UJ0K6w4JQrEoNBXAqtefUPyZAbEiCxkwQQP4AQOiufiHAdH4BfmDgwHRSIa162DdMnYIH8SVAgbea9B4LVAtCzB/fgKa8xM0kfObge3Ofyb2XwxswJKEDVjBg9bKgUb9mKGz77BAQwEAAci0ohUGYRh4s1FUmHsYwze/wP//J59UNhzMDZZrUkUsFPqQQBqONHfpKWkwdlgGyzjJeUEWAGrsz99rFaxNjTxLdZwaV59bWaIs3alnSxxW2HqqWMwffhZPFNFwdYSwVvnTdlgM6e32C3Yin1DV+B7df8TeKaRJDAX5yZDPxonj6xsFIrW7XyADQjEjZB8laaJ85RsZT7y3RiWL/aE7KLl/Aci0uhYAQRhoMZGwd6H///uiCKKgqN12WdDDXhR0H+q2837hZYEAaF+Yoy4tuE9pnW6uyVCAa9vbDP07HZ0Oh6WLKjhkX6XWVhLqN1ItG1YaDsPwMgNV7OnY9FEHc7iiI2UPbxqM3GOmU7H+02E8AUj2gxK24uzbjA4T8Oni24BqmYw92KjTcLoiWZom0TtmcEiMBMhohFsAJq0kB0AQBmJ6MiHeTPiD/3+RP/BgiAZqp4tw8lRoh8LYdgK0/2quJuekyInu2lb0EMC/On6EgAmbFrJkwQ+kkoFPm+b2ggZzekaQB94dcVwpvFEwllIazJeOsbOCWd3F6gBFTR0kgzWuySbCIfMakuUmB7KLbWYbD2r5u2iLqlFqggjLl4U7VMoqnubb3rftMaX5y2Px/glApRXkAAiDMIhZsnjw4v8fZ+ITjLosYVIGTu87sAIbLf2B1lz3Z6+4kEsUNfO4SqK7ZiolccurvpOgLsgcvDyLxw8ReQrFOGjSQaOlwiM80+CUl59BXGDaOglay+40qFQAHCR/I5vJ3hkt1JC4Wx0pPx08lm53lr6og+KugJWmwJmVQWyxaMB5tcHEg1/0W238CMCktawwCAPBbUqgIIh47P//W08VxUejaGMmmUEPOQf2ObMzQok5aI5mX4i/z5uUxSlxpH/34G0dK9vqxr0gGNrki9SK+xYwUZvy8nbcPZGt0/MJNmAgdgwkKk7MHtv1wwCKNH7tArVqeZFKs2spzKw+JYsJAZscpmJ5gJyyhHIISoR+XOLxiwmTPXIcZRNTAeESmFvWin1BDs//KQDTVteDMAgDC1ETX/a+///jfGIGdTPKxrxri+yBhISE0qN83vUfacH4SwXtbPrWPTahMG96BCwC8ZPk+0XSGHDRWGGAEgLuvyTCAnoYKCspdkCo6qnlPhR3dnHnWsRdHdjJ69EBuEl/tGfpKQBzn0b1x/ups6l0d0wIaWHa4piS8wdPtGXYfXyUta8oOckLGL63Agir+bzZN/i3WB4DI68elqbuaT8BuLSWFYZBILimhObSW6E/0P//pPbYBqKnkEgStTPuSqAHQUFE96Hjzvy/ntwOFdFpUEqralnplwMpiv/v7LOE6SIjcOIdiPrqks2YTFIw9AoPHxg/nb49XLUzXUaNgN4ipMGFVs1t9x3T7mvR6c2grYbd/p/5FMYHEsroeyYSjOUw51aUh2AGsGxEqi9gjTfa65D1k8sSSswb7rRd9i0BMHUSeUbE5RyVbFkoV11Pj1Wj/QSg2YpxEIZhoKEszEhI/Q/PZ2dgYGArAiE1odRpAz77MmSwlESRE8c536U5zUshKcCqa1L3UZFaC1cJtde32ESLjK8q70epz+O86TvXtW5Dg400fs2RTYH5LkRx2OmDLfbEx4yH58hT0wqmC8Nyx1M20Cb/Ka14aeN+U8x7hn9rfNHABQ+CBYw89kYZyi6JRoiafbe+t9WRAWipOkvVLOWj3lsnIgINJJCs5RQubyyVO+0vANNWrIQwCEPD6fXOxbG/4+/3Fzp0cNTJVoVCT/C9hKJTDo4hCUkIL8mOgik0Wn7Ow96tDiImlm75wiAPDBGhPyYJr03mxwaLS9L3JR8dBV+dZeAceZiz3TJzN4ajK4vCWJ9ALwfDTlQhdLubWBDf2Qh1f5FWWGkJrTMHuuPsCDqAToQMKzCw1jGN6IwHinnO9lIuVcHP0moIYLVAW2ocHkK8P9o5TiDSU2He+nv/Z6v0d/AVgEkrxmEYhIFQhqCsyS/6/4dUlbp2iaquaRRETKH1YUM7eENgm7MFvutI00waHcaBpsdEfoB62vNmhzNvvgniHhBotyGSfW3erbPNk0sk6ggERNpKqxIRaka2Z5FKu5yE0jsX+VRXtAF1i97frglrz4vma6uOIEsefMCNPb2y3Y2QxaMuBxn3z5WDZMZctsEiSdMCDcVIs5DEoHmkUtkFRJKRqCif9/T5zZ36O+0rANlWkgIgDAOL281n+P/X+ANF8ShUMS51polW8NYNkZBM2snki2mP4ZiYd09jWfVZNFQFYMdmBZmna53LfKVUKqPOguVWb9QopVEswVI21WuWcgPrBNhrMa+xTl13I+rPL8iLS+/LwryMFmJGNR6dVE+P7ww402E8BoW7yGle6R4dXEqwEVLtJVTpPBCsEJqI5BPOeWwhNnSw3ypK7r1h2aI/8WM5bgHYtIIUhkEgaBoChYZAL/lE39L/33sohAYkxRjSRu1Mdo2XnoQFD7urzrgz/6Yc7AtRmP1jxdeWaBLMF+jp580042LsZQjd1Efn2/p6dqmqRrrBiKZBRH/eshiLlEbFlNSKbXghfkciN3W97keTsxuSvWwhzaPWt2aKtAbEHzipT+y1J3EgsVdOU2uUuG6pYEpmPlGKSzjEm5yAWxNWS4vCokVyokz5j1hwSFBWUwDg+IP+BGDTinEYBmEgNFJVNZWydOiU/38pD8hQpZUIpEmVoNA7sKdmgQnLOozPPnMImix0M38QoapJF5H0Jy32+y8q537t5m0PlU/nm491a+2jWVJltSLQbHCVwR+f61PmaXf40iDKWr1ECYN8iMBpa5QnJdim8pmA3QelnUHA0tR3ge1aVBzKiBp1Qt58sSGa5Fazk8jABcN4Mi/wwxsmXCiM+SGAvuQ1BexP7v4JwLbVtCAMw9B0CMLG0JMX2dWD///v7Cqic3Mf0HUbrS9NxkQsFNpbSPPxmrz8rdxqQmDUw2W8GByN2IqH8URMDZ9d7C3Ysp4P+Y5yeOrxYUNxcXQt8PE1TGSJyc4rTgri+GuH8cQ8UJzPVhlDe9pmuljOUbe6fe1EWRXu90U664ORXsA6pJMmmi8UI2ZCDep6Cq+J5t4B5uLhG0MN4FsFlPJEqH23ojQuQnaQZmRSjP+CGL/rIwCdVteDMAgDy/xKNp2Jf8T//4f2wubURZwbgndFND5IQniCpOXaHuX+tbtJ6OY5QVZ1Av7N25hZpiAAGKqol3M3SlmvpS6jVIQ7bIjblTkeqmKhNIR56Ipd1ic9BvVpREDH55dJU7UZ+btuKd8WEAcyzJNSBJzRwJwT1p6cLCSH5d4ML4bVcxM1yuNOmUhE0Ltmb+zFgaXdUAKCMfcpjv0gbevEAn0DHfZIVEPLdfGr8s4djo8DXwLQbQUrCMMwdEkj7qDgSfwBv8L//w9BRDzpqJ24usRkaRk7eC2l0LRJ3kte/rnnZLTSoIY6QghlXQ8n+30mGV1zs9KMGk0kZdjGFK/bLJvTW470VeI3yIxJ6yjsJBRCH07s0OVXUGNbWzbXqgg7jLEitBklses2oiyvguIPpKFg3AUDMvmMcLm3eH2E8PwM0mMeaR/wQEm4v+X0Yu4UycbSjTKEZykDCmWiZuZtCxf9CcC1FeMgDMNAJykQAgMLldj5/4MYGIgYkFooUqQ2Kk3oJbEqmCN5sBzfnX3+Txo/JCJXgIZocaXgCs5vskcVVymwL2Ee6rcZN/t7IL33dDk1n/osxUEycvGcEcUEg/IRO4Q57IhhoMk9KfWzV8kqZFHxUvHyCgl7TJmDjXHpOkVcxJmPOS2iNbKzUl2toFtHonFKOa/DYHaVXpspyGeMw5vafkUtpCFurkCJqxwq+YfL0pi/6A96fgWg21xyEIZhIGrHIgtW3IBLcP9DcAE+2UBVkQVQoSatyeAElQU5wkiOZ14mfxdBEw7KDxWLwsPgA9bTEJIfDVCmyVoVuYbcrkzGaZ9osyLdbbnI0SYP5Bs8Ei4dIuGWBGqAs/gUHhYv7djd1+aC1LREyjjm37BQ0Rk6oZ2jOaw5BOHDRegcSfrIGgfl18wyxpKm7ylH9ko3of7hSgKQYtswD5PtWmcc0dfi8vLN8HveAtBtBisIhUAU1WfwoPqKtv3/p7RpJUibioIKCqecd6+OL1rkSkRdDMPh3tH5x7QeuC4JWRopz+YQqrmX1lDP5ldKWrKOZ/gdL8A5JjP+ZOF2w66BYG8Ka0s7ZguI7A7I26Wp/Vqdp37L9r8Wt5w5x+077I+fZkkZwJebFRSZkaDs4+hiGsP+GHy6+MXpriuAf3jI4OWtRLSUW9ar5lJEsZarz/bwiHNw9IuizrMfucExCSBiFsBAK21wq4vxK0QMPHnHBXEvqIEAW8gJXkDyHzoyAM1wP4F+lAcGnLzwX2AHChTkoDGun1DPg/odoO4VL1CAlRmyYBk82AGk3wD514Fyr4HWX/4DmVEC9Sy+I+If1Kh8DLTzxi+GO4+ZGIAB9v8+0NjXwG7o52/A1jMwwH78Ai/xY/3779/P////M4JbAOAO2T8wBpVhf6GRDhaHBhrIlX//Y6lBAQIQbsU4DMIwME46du8DEP//D0uRWJgqIgEiKo7rw0GiMBApSwYPJ8c+n853oP191cPDVt/mMqB4Aw2CDBSBJRl4GPxZO1iayEVtdGP9ddVrpacHZ4P9fQjmKIrBImE9HwbksJirF8oFWP872z3y88JONBmlfbhOk7DpWdoPSz+JxERZ6xRG5qCJxEx5lUzalZT3g/mQZ8EK+LYHWiShE3CXWrafnwAiJqUhBxyKOCgWvkJ7EL8hDQDQFi5QxQDaFw4qZliZgH27f9BZuL/A9tL/z//VJHj+czGBalXQQqeXoNYpK6Tvygodsv77A1IoPAVlYWCgvvkPKfdgi/WgUQga9bn9l+H9/d8Mj4D1w/M3Xxleff3N+PEH+7+vf5j//AR2mf/+/8f+7z/jH2AC+wLRDNILlPkD3auIBTAyIHqrjNgUAARg5Np1AARhoGiiwubk7P//lTEuLpoQfCBoD2owTv4AgQul17uWv/1p3+Uf5yQApxOVh7toG3Ya+c+NkoCrpMhUbTMl9aXEZLs2J0Ahly/cwQh5B3NSAAvytEHN6rjG9Inr7jH2wW0H4os9RSdhOs6UCYkz6O3w5nTFbjGV5z3dLnSHrnF7ZwTscdpdESjgxc+iY8pxsPD4Pqt4Y3ALQMrZrAAIAkFYCSrq1q33f7W6FJGHhLSyZlyFoGPConjylx0/Xf+E+TBlRxFfpLFMh1EJAXZkURANFmrArAw79KqenCoLw7k/+q5UbaOpNpWI3OZMVwqXsDEOEnJSiaz12OcZVTgcWDjXAbt3hD+ZqeZ3DekQcIjaJB7qjkDgJbEIERY00kTCQUh4w0JCATTnxXiZkr+k+KzHRwBSzqAHYRCGwuu2GOJc9v9/nRc9OjcXlzml+FGY0bNnCIFHee2Dln8qVjbwPq80RbK8yEg+T8Ty9O33FS3unLTbjiicuLbWMfj5uHZNL+3Byd41pVSl2F2NH0MsMcZUJCzoHQW4R8pfV8Z5Il97jOXC+k80n+l+RffM7NiqkxXEAhhe3sHjWzCdL01ek8VOQSOfZWeSNbYBFuvjhyTWv4jgF7i3AKRc0QqAIAycEEk99P+/GBGEEmbD1s0ZvfSW4Itvd2zn3Kl/SXuIe0ZtTbimc2RHMW0UKeYd2MMQkbKZPPdU9kBpnCV6J96PV9dNVgsCvAPcUlg4x/pwX83wgjWBcGZE7brZndlVd0pkc0hCCcTxtaDyG2qYqOXoXiGxqYRxIw1RVr/mEdPksxF3yGvQfpJ2C8DKFeQACMKwiSj//ycmnkAzhnZbTEj06IE7lA62wvoHaJ9ANq+VVW/QNhoHrVFaOq0TU8TE+5EImKDM7hTnSiFULAbggJoXi7kjqNWEIGdgnEyiVzTKDlUhdoCWMbbiWVwFtc3cJBQyptmzkniT7PhFD7togPHp9jsepab6qZb2uGmNouMrPG8BWLmWHQBBGEYw8f9/VWKU6B6uK3j24IEzyegeXTd+N9pI1zaal1ifOXYmBMhhtRD39wm9oeZCz7oEfzXKQAIpLSKyIfUJ2YZEKOqdKPDG3lfDYEG40naRYGvubmrc0dPD59c75TUaj6dwxUed9SRQJkOiUf8wqPwIIGoGGjhW/kPab3/YIb1KYBcPPKEHbriD2m/AAPzOA1rX+o/hy8efDNzA8g10vgE783/4mNA/6KaIH8CUBT5LDZgFP4PG639ARpRBNGj8HrQ4FFS0g05AAOVITugRO0ygoySYkOZtGVE9//8vJFv+hRb+oMgB5YQ/PxGFP14AEEC0yJ7g+eufkHIBVsiC9yB9RJxq9YETtPbtHwMnMLuCTlbgYIau2mWCZusfkDFe8EjqR8hEx+efkMAC127QqRzw2AkHpB/8F3yA3R9waw/UNAYf/gSl/8GWWMCaF9AJQJA9oDlO8GwUA2TE+j+hUAMIIGoHGmxY6Q90pSxoCz+4BgW19bnAB7qA9yCAFpeAepqgtTRc7JAWGng5ABO0afsXOvj5DTKN9uUTdGT1JyTrwNbEggY3WP5AxpPAswgckHXd4CPGGKEzrQyQAIPN40Ln1yHzHT8hoxk/fyP6GwRTGkAA0STQGBjgR239+QIpVcATfD8hw49fWSEHz4GPNmSDbMcA0aCNtqAsBQq039BBUFDX7NtnSGCBAvDHP9Tyhhm6xgI8GgPdw/KPDTL6wgodG2OEdpPAq7eZIE1p0CQKKBX/+oNol/2B9Z0JBRxAANEie8ICDjyu8x86GP0fstUZlAVAKQCU5UAn7IFWXLKxQBYRgrrroG4YqGAGHzj3GzKB/R16wh76/CMD1HzQ7jpQOQoa6wOf4scKGcL6zYg06vqXAXHy3y9IefYLGnB/kCaDYRGCsxIAAYAAolmTA4qRux+wvhwoRkEp6hdoXO47dOfUH0jKAE0jg442hDn8H3QfJvLcI3InmhFqGXgiAbrs7x8XpPaGrZX9Dy0nQeXsH0aEueBN/v8RkyfIZuNNaQABRKtAg4H/aGxYzMMcByqQGaEpBbbyGLZb5D90aAY2poEt2yCnanBLDDpE/58RKcIYIeXXH+hILKywh+lFb48RLNMAAojWgYYO0B0GDkhoSoLNKcE8ADss+D8DqqdwmQkbRARXQMjyjIi1ZWD8HzMyCQYUMgAIIHoHGjpAHnZCzhroI6aEPIUccP8YEBEAAv/+o6ZIdD0kA4AAGuhAAwHk8g8GsA7+EWEOCKAvIyA62xELAAIMADZIQ9NbekdAAAAAAElFTkSuQmCC'
    __explosion1 = BytesIO(base64.b64decode(__explosion1))
    __explosion1 = Image.open(__explosion1)
    __explosion1.save(os.path.join(_resfld,'explosion1.png'))
    __explosion1.close()

if not os.path.isfile(os.path.join(_resfld,'ufo.png')):
    __ufo = b'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'
    __ufo = BytesIO(base64.b64decode(__ufo))
    __ufo = Image.open(__ufo)
    __ufo.save(os.path.join(_resfld,'ufo.png'))
    __ufo.close()

if not os.path.isfile(os.path.join(_resfld,'fighter.png')):
    __fighter = b'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'
    __fighter = BytesIO(base64.b64decode(__fighter))
    __fighter = Image.open(__fighter)
    __fighter.save(os.path.join(_resfld,'fighter.png'))
    __fighter.close()

if not os.path.isfile(os.path.join(_resfld,'thunder.png')):
    __thunder = b'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'
    __thunder = BytesIO(base64.b64decode(__thunder))
    __thunder = Image.open(__thunder)
    __thunder.save(os.path.join(_resfld,'thunder.png'))
    __thunder.close()

    
if not os.path.isfile(os.path.join(_resfld,'bug.png')):
    __bug = b'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'
    __bug = BytesIO(base64.b64decode(__bug))
    __bug = Image.open(__bug)
    __bug.save(os.path.join(_resfld,'bug.png'))
    __bug.close()

# 以下是小猫的朝右造型
if not os.path.isfile(os.path.join(_resfld,'cat1.png')):
    __cat1 = b'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'
    __cat1 = BytesIO(base64.b64decode(__cat1))
    __cat1 = Image.open(__cat1)
    __cat1.save(os.path.join(_resfld,'cat1.png'))
    __cat1.close()
    
if not os.path.isfile(os.path.join(_resfld,'cat2.png')):
    __cat2 = b'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'
    __cat2 = BytesIO(base64.b64decode(__cat2))
    __cat2 = Image.open(__cat2)
    __cat2.save(os.path.join(_resfld,'cat2.png'))
    __cat2.close()


# 以下是小猫的朝左造型
if not os.path.isfile(os.path.join(_resfld,'cat1_l.png')):
    __cat1_l = b'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'
    __cat1_l = BytesIO(base64.b64decode(__cat1_l))
    __cat1_l = Image.open(__cat1_l)
    __cat1_l.save(os.path.join(_resfld,'cat1_l.png'))
    __cat1_l.close()
    
if not os.path.isfile(os.path.join(_resfld,'cat2_l.png')):
    __cat2_l = b'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'
    __cat2_l = BytesIO(base64.b64decode(__cat2_l))
    __cat2_l = Image.open(__cat2_l)
    __cat2_l.save(os.path.join(_resfld,'cat2_l.png'))
    __cat2_l.close()

if not os.path.isfile(os.path.join(_resfld,'ball.png')):
    __ball = b'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'
    __ball = BytesIO(base64.b64decode(__ball))
    __ball = Image.open(__ball)
    __ball.save(os.path.join(_resfld,'ball.png'))
    __ball.close()
    
if not os.path.isfile(os.path.join(_resfld,'sky.png')):
    __sky = b'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'
    __sky = BytesIO(base64.b64decode(__sky))
    __sky = Image.open(__sky)
    __sky.save(os.path.join(_resfld,'sky.png'))
    __sky.close()
    
if not os.path.isfile(os.path.join(_resfld,'b1.png')):
    __b1 = b'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'
    __b1 = BytesIO(base64.b64decode(__b1))
    __b1 = Image.open(__b1)
    __b1.save(os.path.join(_resfld,'b1.png'))
    __b1.close()

if not os.path.isfile(os.path.join(_resfld,'b2.png')):
    __b2 =b'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'
    __b2 = BytesIO(base64.b64decode(__b2))
    __b2 = Image.open(__b2)
    __b2.save(os.path.join(_resfld,'b2.png'))
    __b2.close()


# 以下定义屏幕的鼠标移动事件
def __onmousemove(self, fun, add=None):
    """绑定鼠标移动事件"""
    
    if fun is None:
        self.cv.unbind("<Motion>" )
    else:
        def eventfun(event):
            x, y = (self.cv.canvasx(event.x)/self.xscale,
                    -self.cv.canvasy(event.y)/self.yscale)
            fun(x, y)
        self.cv.bind("<Motion>", eventfun, add)

def _onmousemove(self,fun,add=None):
    """绑定鼠标移动事件"""
    self.__onmousemove(fun,add)

TurtleScreenBase.__onmousemove = __onmousemove
TurtleScreenBase.onmousemove = _onmousemove

# 重定义_drawimage方法
def _drawimage(self, item, pos, image):
    """在画布x,y坐标重新配置image
    """
    x, y = pos
    self.cv.coords(item, (x * self.xscale, -y * self.yscale))
    self.cv.itemconfig(item, image=image)
    self.cv.tag_raise(item)
TurtleScreenBase._drawimage = _drawimage

def mouse_pos():
    """获取相对于海龟屏幕的鼠标指针坐标，和屏幕的缩放参数scale无关。"""
    screen = Screen()            # 新建或返回屏幕对象
    _root = screen._root
    abs_coord_x = _root.winfo_pointerx() - _root.winfo_rootx()
    abs_coord_y = _root.winfo_pointery() - _root.winfo_rooty()
    x =  abs_coord_x - screen.window_width() //2
    y =  screen.window_height() //2 - abs_coord_y
    screen.cv.update()
    return (x-3),(y+3)

mouse_posisiton = mouse_pos
mouseposition = mouse_pos
mousepos = mouse_pos
getmousepos = mouse_pos
getmouseposition = mouse_pos


# 以下定义屏幕的鼠标松开事件
def __onscreenrelease(self, fun, num=1, add=None):
    """绑定鼠标的松开事件，默认为鼠标左键，即num为1。
 
    """
    if fun is None:
        self.cv.unbind("<ButtonRelease-%s>" % num)
    else:
        def eventfun(event):
            x, y = (self.cv.canvasx(event.x)/self.xscale,
                    -self.cv.canvasy(event.y)/self.yscale)
            fun(x, y)
        self.cv.bind("<ButtonRelease-%s>" % num, eventfun, add)

def _onscreenrelease(self, fun, btn=1, add=None):
    """绑定鼠标的松开事件，默认为鼠标左键，即num为1。
    """
    self.__onscreenrelease(fun, btn, add)

TurtleScreenBase.__onscreenrelease = __onscreenrelease
TurtleScreenBase.onscreenrelease = _onscreenrelease

# 以下重定义screen的reset方法
def __TSreset(self):
    """重置除了说话泡泡海龟外的对象到初始状态。    
    """
    for turtle in self._turtles:      
        if turtle.tag != 'bubble':
           turtle._setmode(self._mode)
           turtle.reset()
TurtleScreen.reset = __TSreset

# 产生一个颜色表，里面的颜色较鲜艳
def makecolors(n=128):
        
    """产生颜色表，饱和度和亮度最高，所以很鲜艳"""
    cs = []
    for y in range(n):
        x = random.random()
        r,g,b = colorsys.hsv_to_rgb(x,1,1)
        r,g,b = int(r*255),int(g*255),int(b*255)
        cs.append((r,g,b))
    cs = ["#{:02x}{:02x}{:02x}".format(r,g,b) for r,g,b in cs]
    cs = list(set(cs))
    return cs
_colorlist = makecolors()    # 产生一个颜色表

        
class Clock:
    """控制fps的时钟Clock类"""
    def __init__(self):
       self._old_start_time = time.perf_counter()
       self._start_time = time.perf_counter()

    def tick(self,fps=0):
        """返回每帧逝去的时间，如果fps不为0，则会等待直到时间大于1/fps"""
        end_time = time.perf_counter()
        elapsed_time = end_time - self._start_time

        if fps!=0:
            step = 1/fps
            if elapsed_time < step:  # 如果逝去的时间小于step则等待
               time.sleep(step - elapsed_time)
            
        self._old_start_time = self._start_time
        self._start_time = time.perf_counter()
        return time.perf_counter() - self._old_start_time
    
    def getfps(self):
        """得到fps"""
        t = time.perf_counter() - self._old_start_time
        return round(1/t,2)

# 产生爆炸效果的函数，需要传递图像帧
def explode(pos,frames,interval=100):
    """pos坐标位置产生爆炸效果,frames:就gif序列帧"""
    t = Turtle(visible=False)        # 实例化一个对象
    t.penup()                        # 抬起笔来
    t.speed(0)                       # 速度为最快
    t.goto(pos)                      # 坐标定位置
    t.st()                           # 显示出来
    t.index = 0                      # 表示造型索引
    t.frames = frames                # 所有造型
    t.amounts = len(frames)          # 造型数量
    def animation():                 # 切换动画函数
        if t.index < t.amounts:
            t.shape(t.frames[t.index])
            t.index = t.index + 1
            t.screen.ontimer(animation,interval)
        else:            
            t.ht()
            t.screen.cv.delete(t.turtle._item)
            t.screen._turtles.remove(t)
    animation()

_built_in_images = ["bug.png","ball.png",'cat1.png','cat2.png','cat1_l.png','cat2_l.png',
              'b1.png','b2.png','fighter.png','thunder.png','ufo.png','explosion0.png',
              'explosion1.png','sky.png']
_built_in_images = [os.path.join(_resfld,cms) for cms in _built_in_images]

class Sprite(Turtle):
    """
       继承自Turtle的精灵类。
       
    """
 
    # 预制造型图，减少对图像文件的读取
    imdict = {}       
    def __init__(self,shape=os.path.join(_resfld,'bug.png')
                 ,pos=(0,0),visible=True,undobuffersize=1000):
        """
           shape：造型图像(int或str)，pos：起始坐标，visible：可见性，undobuffersize：可撤销次数。
           新建一个精灵，默认为小虫子，在屏幕中央。
        """
        Turtle.__init__(self,visible=visible,undobuffersize=undobuffersize,shape='blank')
        self._rotatemode = 0                            # 设定旋转模式，0:360度旋转,1:左右翻转,2:不旋转
        self.im = None                                  # 存储原始图形的im属性
        if isinstance(shape,int):
           shape = min(len(_built_in_images)-1, max(0, shape))
           shape = _built_in_images[shape]
        else:
          if shape not in self.screen._shapes and not os.path.isfile(shape): shape='turtle'        
        self._position = Vec2D(*pos)
        self.shape(shape)
        if visible : self.st()
            
        self.onclick(self._store, 1)    
        self.ondrag(self.drag,1)        
        self.tag = 'sprite'                              # 贴一个标签
        self._sayend = True                              # 初始状态的说话结束 
        self._saycolor = "#303030"                       # 说话的字的颜色
        self._saybordercolor = "#CCCCCC"                 # 说话的字的泡泡边框的颜色        
        self._draw_bubble_turtle = Turtle(visible=False) # 用来画框写字的龟
        self.screen._turtles.remove(self._draw_bubble_turtle)
        self._draw_bubble_turtle.up()                    # 抬起笔来        
        self._draw_bubble_turtle.speed(0)                # 速度最快        
        self._draw_bubble_turtle.pensize(3)
        # 以下防止在使用screen.mode调用reset时显示出来用的
        self._draw_bubble_turtle.tag = 'bubble'          # 标志为说话泡泡海龟

    def rotatemode(self,mode=None):
      """设定旋转模式，无参时返回当前旋转模式。
         0:360度旋转,1:左右翻转,2:不旋转
      """
      if mode == None:
        return self._rotatemode
      if mode <= 0 :
        self._rotatemode = 0
      elif mode >= 2:
        self._rotatemode = 2
      else:
        self._rotatemode = 1
      
      
    def collidemouse(self):
      """碰到鼠标指针的检测"""
      left,top,right,bottom = self.bbox()
      xscale = self.screen.xscale
      yscale = self.screen.yscale
      left,top,right,bottom = left*xscale,top*yscale,right*xscale,bottom*yscale
      
      mx,my = mouse_pos()
      c = mx<= right and mx >= left and my <= top and my >= bottom
      return c
      

    def _store(self,x,y):
        self.clickpos = Vec2D(x,y)
        
    def drag(self,x,y):
        """拖动自己到鼠标指针的坐标"""

        self.ondrag(None)
        neu = Vec2D(x,y)
        self.goto(self.pos() + (neu-self.clickpos))
        self.clickpos = neu
        self.screen.cv.tag_raise(self.turtle._item)
        self.ondrag(self.drag,1)                      
        
    def reset(self):
        Turtle.reset(self)
        self._rotate(0)
        
    def _loadim(self,image):
        # 原始图形,最好面向右
        self.imagebasename = os.path.basename(image)
        if self.imagebasename not in Sprite.imdict:   # 不在这个字典中则第一次加载
            self.im = Image.open(image)
            self.im = self.im.convert('RGBA')
            # for rotatemode 
            im_mirror = ImageOps.mirror(self.im) # 镜像造形
            self.rightleftcostume = [self.im,im_mirror]
            Sprite.imdict[self.imagebasename] = [self.im,im_mirror]         
            
        else:                              # 在这个字典中,则不读文件,直接从字典中取数据
            self.im = Sprite.imdict[self.imagebasename][0]             # 向右造型            
            self.rightleftcostume =  Sprite.imdict[self.imagebasename] #  向右向左造型
        
    def shape(self,name=None):
        """重定义shape方法"""
        # 如果名字为空,则返回形状的名称
        if name==None:return Turtle.shape(self,name)

        # 如果名字在形状字典中,而且不是文件.
        if name in self.screen._shapes and not os.path.isfile(name):
            Turtle.shape(self,name)            
            self.onclick(self._store, 1) 
            self.ondrag(self.drag)
            return        

        if os.path.isfile(name):self._loadim(name)
            
        heading = self.heading()           
        stretch_wid,stretch_len ,w = Turtle.shapesize(self)   # 获取缩放值
        new_name = str(stretch_wid) + "_" + str(stretch_len) + "_" + str(heading) + self.imagebasename
        if os.path.isfile(name):name=new_name
        
        if  new_name==name :
            if new_name not in self.screen._shapes:
                newwidth = max(1,int(self.im.width * stretch_len))
                newheight = max(1,int(self.im.height * stretch_wid))                
                im = self.im.resize((newwidth,newheight),Image.ANTIALIAS)
                if self._rotatemode == 0:                    # 360度旋转
                   im = im.rotate(heading,expand=1)
                   
                elif self._rotatemode == 2 :                 # 不旋转
                   pass
                elif self._rotatemode == 1:                  # 左右翻转
                     m = self.screen.mode()
                     if m == 'standard' or m == 'world':
                        if heading < 270 and heading > 90:
                           index = 1
                        else:
                           index = 0
                     else:
                        if heading < 180 and heading > 0:
                           index = 0
                        else:
                           index = 1                   
                     im = self.rightleftcostume[index]
                     im = im.resize((newwidth,newheight),Image.ANTIALIAS)
                
                shape = Shape('image',ImageTk.PhotoImage(im))
                self.screen.addshape(new_name,shape)
                
            Turtle.shape(self,new_name)
            
            self.onclick(self._store, 1) 
            self.ondrag(self.drag)         

    def _go(self, distance):
        """重定义_go方法,移动指定距离"""
        ende = self._position + self._orient * distance
        self._goto(ende)
        
    def _rotate(self,angle):
        """seth,right,left最终都要调用它，所以重写它就行了"""
        
        Turtle._rotate(self,angle)         # 调用父类的同名方法
        if self.turtle._type in ['polygon','compound']: return
        if self.shape() == 'blank':return
        
        heading = self.heading()           
        stretch_wid,stretch_len ,w = Turtle.shapesize(self)   # 获取缩放值
        new_name = str(stretch_wid) + "_" + str(stretch_len) + "_" + str(heading) + self.imagebasename
        
        self.shape(new_name)        

    def shapesize(self,stretch_wid=None, stretch_len=None, outline=None):
        """重定义缩放形状方法"""
        x = Turtle.shapesize(self,stretch_wid,stretch_len,outline)
        if hasattr(self,'im') and self.turtle._type == 'image':         
           new_name = str(stretch_wid) + "_" + str(stretch_len) + "_" + str(self.heading()) + self.imagebasename      
           self.shape(new_name)
        return x
    
    def addx(self,dx):
        """横向坐标增加dx"""
        self._goto(Vec2D(self._position[0] + dx, self._position[1]))
         
    def addy(self,dy):
        """纵向坐标增加dy"""
        self._goto(Vec2D(self._position[0], self._position[1] + dy))
        
    def scale(self,s=None):
        """按比例缩放角色的造型"""
        if s == None:
           return self.shapesize()
        else:
           self.shapesize(s,s)

    def gotorandom(self):
        """到随机坐标"""
        sw = self.screen.window_width()
        sh = self.screen.window_height()
        x = random.randint(-sw//2,sw//2)
        y = random.randint(-sh//2,sh//2)
        self.goto(x,y)
        
    def bbox(self,item=None):
        """获取画布上对象item的绑定盒"""
        if item == None: item = self.turtle._item

        xscale = self.screen.xscale
        yscale = self.screen.yscale
        
        if isinstance(item,int):
          box = self.screen.cv.bbox(item)
          if box == None :return
          x0,y0,x1,y1 = box
          left,top,right,bottom = x0/xscale,-y0/yscale,x1/xscale,-y1/yscale
          
        else:
          box = []
          for i in item:
            b = self.screen.cv.bbox(i)
            if b == None : return
            x0,y0,x1,y1 = b
            x0,y0,x1,y1 = x0/xscale,-y0/yscale,x1/xscale,-y1/yscale         
            box.append((x0,y0,x1,y1))
            left = min( [a for a,b,c,d in box] )
            top = max( [b for a,b,c,d in box] )
            right = max( [c for a,b,c,d in box] )
            bottom = min( [d for a,b,c,d in box] )           
        
        return left,top,right,bottom
    
    def collide(self,other):
        """和其它对象的矩形碰撞检测，
           other可能是海龟对象或者一个项目item编号，如图章。
        """
       
        # 自己的左上右下值
        x0,y0,x1,y1 = self.bbox()
        _left0 = x0
        _top0 = y0
        _right0 = x1
        _bottom0 = y1

        # other要么是其它海龟对象，也可以是个图章！
        if isinstance(other,Turtle):
           item = other.turtle._item
        else:
           item = other

        box = self.bbox(item)
        if box == None :return
        _left1,_top1,_right1,_bottom1 = box

        nocollide = _right0 < _left1 or _left0 > _right1 or \
                    _bottom0 > _top1 or _top0 < _bottom1
        return not nocollide        
        
    def heading(self,other=None):
        """获取朝向，或者朝向某个对象与坐标位置。"""
        if other == None :
            return Turtle.heading(self)
        if isinstance(other,Turtle):   # 如果other是海龟对象
            x1,y1 = other.position()   # 获取它的坐标
        elif isinstance(other,tuple) or isinstance(other,list):
            x1,y1 = other
        self.setheading(self.towards(x1,y1))

    def randomcolor(self):
        """设定随机颜色"""
        c = random.choice(_colorlist)
        self.color(c)

    def randomheading(self):
        """设定随机方向"""
        fx = random.randint(1,360)
        self.setheading(fx)
        
    def _display_bubble(self,item):      
        """画说话泡泡"""
        margin = 10
        r = 10
        rect = self.bbox(item)
        if rect == None : return
        left,top,right,bottom = rect
        mode = self.screen.mode()
        if mode=='standard':
          pass
        else:
          self._draw_bubble_turtle.setheading(90)
        
        left = left - margin
        right = right + margin
        top = top + margin
        bottom = bottom - margin
        self._draw_bubble_turtle.color(self._saybordercolor)
        width = right - left
        centerx = left + width//2
        self._draw_bubble_turtle.goto(left+r,top)    # 1 左上角右偏r点
        self._draw_bubble_turtle.pendown()
        self._draw_bubble_turtle.goto(right-r,top)   # 2 右上角左偏r点
        self._draw_bubble_turtle.circle(-r,90)       # 右上角圆角，方向变为向下
        self._draw_bubble_turtle.goto(right,bottom+r)# 3 右下角上偏r点
        self._draw_bubble_turtle.circle(-r,90)       # 右下角圆角，方向变为向左
        self._draw_bubble_turtle.goto(centerx + r*2,bottom) # 4 中下 右偏2r点
        
        self._draw_bubble_turtle.circle(2*r,90)      # 方向变为向下
        self._draw_bubble_turtle.right(180)
        #self._draw_bubble_turtle.circle(-r//5,180)  # 最底下的圆角，方向为向上了        
        self._draw_bubble_turtle.circle(2*r,90)      # 方向为向左了 
        
        self._draw_bubble_turtle.goto(left+r,bottom) # 5 左下角 右偏r点
        self._draw_bubble_turtle.circle(-r,90)       # 向右画1/4圆，方向为向上了 
        self._draw_bubble_turtle.goto(left,top-r)    # 6 左上角 下偏r点
        self._draw_bubble_turtle.circle(-r,90)       # 向右画1/4圆，方向为向右了
        
        self._draw_bubble_turtle.up()

    def _redraw_say(self):
        """重画字和说话泡泡"""
        self._draw_bubble_turtle.clear()      # 擦除以前所说的话
        self.screen.tracer(False)
        left,top,right,bottom = self.bbox()   # 自己的绑定盒子 
        centerx = left + (right - left)//2
        top = top + 40
        self._draw_bubble_turtle.goto(centerx,top)        
        self._draw_bubble_turtle.color(self._saycolor)   # 要说的话的背景色          
        item = self._draw_bubble_turtle.write(self._sayinfo,align='center')
        
##        self._draw_bubble_turtle.goto(centerx-1,top+1)
##        self._draw_bubble_turtle.color(self._saycolor) # 要说的话的颜色
##        self._draw_bubble_turtle.write(self._sayinfo,align='center')
        
        self._display_bubble(item)           # 画说话泡泡框
        self.screen.tracer(True)        
      
    def _wait_say(self):        
        """不断地判断是否改变了坐标,变了就得重画,否则干等"""
        if self._sayend == True : return
        if time.time() -  self._begin_bubble_time < self._saytime:
           # 如果坐标改变了,那么重画说话泡泡和字
           if abs(self.xcor() - self._oldsay_x) > 0 or \
              abs(self.ycor() - self._oldsay_y) > 0 or \
              self.bbox() != self._oldbox :  
              self._oldsay_x = self.xcor()
              self._oldsay_y = self.ycor()
              self._oldbox = self.bbox()
              self._redraw_say()
           self.screen.ontimer(self._wait_say,100)
        else:           
           self._sayend = True
           self._sayinfo = ""
           self._draw_bubble_turtle.clear()
           
    def say(self,info='你好',delay=2,wait=True):
        """在头顶上显示要说的话 ,默认为阻塞进程。"""
        if len(info)<6:info = "  " + info + "  "
        self._sayend = False          # 描述说话是否结束
        self._sayinfo = info
        self._saytime = delay
        self._begin_bubble_time = time.time()
        #  用于改变位置了才重画的三个变量
        self._oldsay_x = self.xcor()
        self._oldsay_y = self.ycor()
        self._oldbox = self.bbox()   # 绑定盒变了也要重画
        self._redraw_say()
        self._wait_say()
        # 如果wait为真，则阻塞程序的运行
        if wait :               
           while time.time() - self._begin_bubble_time < self._saytime:
              print
              self.screen.update()
              
    def saycolor(self,color=None):
        """说话的颜色，如果无参数，则返回当前说话的字的颜色"""
        if color == None:return self._saycolor
        self._saycolor = color
        if not self._sayend: self._redraw_say()

    def saybordercolor(self,color=None):
        """说话泡泡边框的颜色，如果无参数，则返回当前说话泡泡边框的颜色"""
        if color == None:return self._saybordercolor
        self._saybordercolor = color
        if not self._sayend: self._redraw_say()   
      
    def remove(self):
        """从海龟列表_turtles中移除"""
        sc = self.screen
        if self not in sc._turtles:return
        self._draw_bubble_turtle.clear()        
        sc.cv.delete(self._draw_bubble_turtle.turtle._item) # 从画布上删除说话泡泡的形状(虽然它是隐藏的)            
        sc.cv.delete(self.turtle._item)                     # 从画布上删除自己的形状
        sc._turtles.remove(self)                            # 在屏幕的_turtles列表中移除自己
     
        
    def stampgoto(self,sitem,x,y):
        """图章定位到x,y坐标"""
        shape = self.screen._shapes[self.turtle.shapeIndex]
        #print(shape._type)
        if shape._type == 'compound':
          print("sorry,compound shape are temporarily not supported。")
          print("不好意思，复合图形暂不支持。")
          return 
          
        if sitem not in self.stampItems: return
        canvas = self.screen.cv
        xscale = self.screen.xscale
        yscale = self.screen.yscale
        if isinstance(sitem,int):
            canvas.coords(sitem,(x * xscale, - y * yscale))
        else:
            for item in sitem:
               canvas.coords(item,(x * xscale,- y * yscale))
             
    def stampmove(self,sitem,dx,dy):
        """移动图章dx和dy的距离，别名movestamp"""
        shape = self.screen._shapes[self.turtle.shapeIndex]
          
        if sitem not in self.stampItems: return
        
        xscale = self.screen.xscale
        yscale = self.screen.yscale
        
        if isinstance(sitem,int):
            self.screen.cv.move(sitem,xscale * dx,- yscale * dy)
        else:
          for item in sitem:
            self.screen.cv.move(item,xscale * dx,- yscale * dy)              
            
    def collide_edge(self,item=None):
        """检测自己或自己的图章是否碰到边缘"""
        box = self.bbox(item)
        if box == None: return
        left,top,right,bottom = box
        sw = self.screen.window_width()
        sh = self.screen.window_height()
        c1 = left <= -sw//2
        c2 = right >= sw//2
        c3 = top >= sh//2
        c4 = bottom <= -sh//2
        return c1 or c2 or c3 or c4

    def bounce_on_edge(self):
        """当角色用fd命令前进时，配合这个命令让角色自动碰到边缘就反弹"""
        if self not in self.screen._turtles: return
        mode = self.screen.mode()
        hd = self.heading()
        left,top,right,bottom = self.bbox()
        sw = self.screen.window_width()
        sh = self.screen.window_height()
        c1 = left < -sw//2
        c2 = right > sw//2
        
        c3 = top > sh//2
        c4 = bottom < -sh//2
        
        if (c1 or c2) and (c3 or c4): # 同时碰到反转
            self.right(180)
            return
        if c1 or c2:                  # 根据screen模式需要加代码
          self.setheading(180-hd)
          return 
        elif c3 or c4:
          self.setheading(0-hd)
     
    def shapeindex(self,index=0):
      """设定造型编号,子类重写"""
      pass
      
    def nextshape(self):
      """下一个造型,待子类重写"""
      pass

    def flipshape(self):
      """翻转造型,待子类重写"""
      pass
      
    def useshapes(self,index=0):
      """
         设定使用向右序列造型还是向左序列造型，
         0代表向右序列造型，1代表向左序列造型。
         待子类重写
      """
      pass
    def clone(self):
        """重定义clone方法，无参。
        在同一位置创建并返回属坐标、朝向等属性一致的对象。
        举例 (假设有一个海龟对象叫mick):
        mick = Turtle()
        joe = mick.clone()
        """
        screen = self.screen
        self._newLine(self._drawing)

        turtle = self.turtle
        self.screen = None
        self.turtle = None  # too make self deepcopy-able

        # added，对象不能深度复制，所以需要先保存，清为None，再deepcopy
        old_draw_bubble_turtle = self._draw_bubble_turtle
        old_im = self.im
        self._draw_bubble_turtle = None # too make self deepcopy-able
        self.im = None
        
        q = deepcopy(self)

        self.screen = screen
        self.turtle = turtle

        # added
        self._draw_bubble_turtle = old_draw_bubble_turtle
        self.im = old_im               

        q.screen = screen
        q.turtle = _TurtleImage(screen, self.turtle.shapeIndex)

        # added
        q.im = old_im
        q._draw_bubble_turtle = Turtle(visible=False) # 用来画框写字的龟
        screen._turtles.remove(q._draw_bubble_turtle)
        q._draw_bubble_turtle.up()                    # 抬起笔来        
        q._draw_bubble_turtle.speed(0)                # 速度最快        
        q._draw_bubble_turtle.pensize(2)
        # 以下防止在使用screen.mode调用reset时显示出来用的
        q._draw_bubble_turtle.tag = 'bubble'          # 标志为说话泡泡海龟

        screen._turtles.append(q)
        ttype = screen._shapes[self.turtle.shapeIndex]._type
        if ttype == "polygon":
            q.turtle._item = screen._createpoly()
        elif ttype == "image":
            q.turtle._item = screen._createimage(screen._shapes["blank"]._data)
        elif ttype == "compound":
            q.turtle._item = [screen._createpoly() for item in
                              screen._shapes[self.turtle.shapeIndex]._data]
        q.currentLineItem = screen._createline()
        q._update()
        return q

    # 定义别名
    def show(self):
        self.st()
        
    def hide(self):
        self.ht()

    movestamp = stampmove          # 移动图章
    randompos = gotorandom         # 随机坐标
    randomposition = gotorandom    # 随机坐标
    random_pos = gotorandom        # 随机坐标
    random_position = gotorandom   # 随机坐标 
    goto_random = gotorandom       # 随机坐标


# 定义类的别名
Js  = Sprite
Juese = Sprite
角色 = Sprite
精灵 = Sprite

        
class Key:
    def __init__(self,key):
        self.screen = Screen()
        self.key = key
        self.down = False
        self.screen.onkeypress(self.press, key)
        self.screen.onkeyrelease(self.release, key)
        
    def press(self):
        self.down = True

    def release(self):
        self.down = False                

class Mouse:
    def __init__(self,number=1):
      screen = Screen()
      self.number = number
      self.down = False
      screen.onclick(self.press,number)
      screen.onscreenrelease(self.release,number)

    def press(self,x,y):
      self.down = True
      
    def release(self,x,y):
      self.down = False

class AnimatedSprite(Sprite):
  """继承自Sprite的动画角色类"""
  def __init__(self,rightframes=[os.path.join(_resfld,'cat1.png'),os.path.join(_resfld,'cat2.png')],
               leftframes=[os.path.join(_resfld,'cat1_l.png'),os.path.join(_resfld,'cat2_l.png')],
               pos=(0,0),visible=True,undobuffersize=1000):
     Sprite.__init__(self,shape='blank',visible=visible,pos=pos,undobuffersize=undobuffersize)
     self.costumes_amounts = len(rightframes)
     self.costumes_r = rightframes    
     self.costumes_l = leftframes
     self.costumes = [self.costumes_r,self.costumes_l]
     self.costume_r_l_index = 0   # 右左帧序列索引为0的序列号
     self.costume_index = 0       # 帧序列的索引为0的帧号
     self.goto(pos)
     self.shape(self.costumes[0][0])     
     if visible:self.st()         # 如果是可见的则显示

  def reset(self):
    """重写复位方法"""
    Sprite.reset(self)
    self.up()
     
  def shapeindex(self,index=0):
    """设定造型编号"""
    self.shape(self.costumes[self.costume_r_l_index][index % self.costumes_amounts])
    
  def nextshape(self):
    """下一个造型"""
    self.costume_index = self.costume_index + 1
    self.costume_index = self.costume_index %  self.costumes_amounts
    self.shapeindex(self.costume_index)

  def flipshape(self):
    """翻转造型"""
    self.costume_r_l_index += 1
    self.costume_r_l_index %= 2
    self.shapeindex(self.costume_index)
    
  def useshapes(self,index=0):
    """
      设定使用向右序列造型，还是向左序列造型，
       0，代表向右序列造型，1代表向左序列造型。
    """
    index = index % 2
    self.costume_r_l_index = index
    self.shapeindex(self.costume_index)

  # 定义别名
  costumeindex = shapeindex  # 设定造型编号
  nextcostume = nextshape    # 下一个造型
  flipcostume = flipshape    # 翻转造型
  usecostumes = useshapes    # 使用向右或向左序列造型

# 定义动画精灵类的别名
Sprite2 = AnimatedSprite

print("import successful! writed by lixingqiu,email:406273900@qq.com")

if __name__ == "__main__":

    cat = Sprite(shape='blank')
    cat.setheading(90)
      

