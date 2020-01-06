Python sprites  is a module for make game and animation easily.anybody can make game and animation funny. 
It's developed with Turtle module and provide Sprite class mainly 。
In order to facilitate the beginners to make games, some functions are added,
such as Clock class can fix FPS, stamp can move, image can rotate, and support transparent。
it can detect keyboard keys and mouse keys a loop statement,
and add rectangle collision method. There are also functions such as bounce_on_edge and say functions.

Main application scenarios:
1、Introduction to children's computer games and animation development.
2、learn the ABC of Python game development.
3、Python game crash.
4、Getting started with Python for training institutions.
5、Python experience courses and public welfare courses of training institutions.


'''Example one:'''

from sprites import * 

s = Sprite()           # default is a bug

while True:
   s.fd(10)
   s.bounce_on_edge()   

-----------------------------------------------------
'''Example two:'''

from sprites import * 

frames = ['res/cat1.png','res/cat2.png']

cat = Sprite(shape=frames)

while True:
    cat.fd(10)
    cat.nextcostume()
    cat.bounce_on_edge()

-----------------------------------------------------
'''Example three:'''

from sprites import *

button = Sprite('button1.png')

while 1:
  if button.collidemouse():    
    button.shape('button1.png')
  else:    
    button.shape('button2.png')
     
-----------------------------------------------------

'''Example four:'''

from sprites import *

cat1 = Sprite(2)            # is a cat
cat1.say()                    # default is say hello 

cat2 = Sprite(2)         
cat2.fd(100)
cat2.rotatemode(1)
cat2.setheading(180)

cat2.say('你也好',delay=1000,wait=True) 

cat1.screen.exitonclick()
-----------------------------------------------------

more example,please conatct lixingqiu, wechat:scratch8,website:www.lixingqiu.com

sprites module Developer: Li Xingqiu，email:406273900@qq.com,Pingxiang, Jiangxi, China.

精灵模块主要用海龟模块进行开发。为方便制作游戏与动画而设计的一个模块。主要提供了Sprite类，它提供或重写了海龟类的以下方法：
   1、rotatemode：返回或设置旋转模式。 参数为整数,0代表能360度旋转,1代表只能左右翻转,2为不旋转。  
   2、addx：x坐标增加。
   3、addy：y坐标增加。
   4、scale：缩放，只有一个参数。
   5、gotorandom：到随机位置。
   6、heading：重定义了这个方法，不带参数能获取当前朝向。带参数参让角色朝向某对象或坐标。
   7、show：显示对象，带参数时让角色显示一定的时间后又会隐藏，异步执行。
   8、hide：隐藏对象，带参数时让角色隐藏一定的时间后又显示，异步执行。
   9、mouse_pos：获取鼠标指针坐标。
   10、move：移动水平dx距离和垂直dy距离。
   11、collide：和另一个角色或图章的碰撞方法，采用的是矩形碰撞，可以有scale参数，表示缩放绑定盒子，如scale=0.5时，绑定盒宽高各缩一半。
   12、collidemouse：碰到鼠标指针。
   13、collide_edge：碰到边缘检测。
   14、bounce_on_edge：碰到边缘就反弹，适合于用fd命令让角色前进后再使用。
   15、bbox：获取角色绑定盒，也可获取图章的绑定盒。
   16、randomcolor：随机颜色，较鲜艳。
   17、randomheading：随机方向。
   18、remove：移除方法,把自己从屏幕的_turtles列表中删除，并根据item号删除自己在画布上的形状，清除说话泡泡对象。
   19、stamp：重定义了Turtle类的图章方法，新增的参数可以让图章在一定时间后自动被清除，异步执行。
   20、stampmove：根据图章编号水平和垂直移动图章。
   21、stampgoto：移动图章编号到指定坐标，暂不支持复合图形的图章，它们的图章编号是一个元组。
   22、play：播放方法，目前只支持播放无损压缩的wav音频文件，支持显示歌词。
   23、setalpha：设置透明度方法。参数为从0到255的数值。0代表完全透明，255代表不透明，128代表半透明。
       对于polygon和compound造型来说，0代表透明，非0代表不透明。对于image来说，设置角色的透明度从0到255的值就会产生从透明到不透明的渐变效果。
   24、getalpha：得到透明度，从0到255的整数。
   25、set_tag：设置角色的标签。它是一个字符串，用于分组。
   26、get_tag：获取角色的标签。
   27、say：说话方法，会显示气泡。默认时间为2秒，默认阻塞进程。
   28、saycolor：返回或设置说话的字的颜色。
   29、saybordercolor：返回或设置说话泡泡的边框颜色。   
   30、write：重定义写方法，增加angle参数，可以写斜字，默认为黑体，12号。
   31、reborn：“重生”方法，让角色隐藏后在另一坐标重新显示。复用角色之用，可加delaytime参数，意为在一定的时间后才显示，异步执行。
   32、nextcostume：下一个造型，别名是nextshape。
   33、previouscostume：下一个造型，别名是nextshape。
   34、costumeindex：指定造型编号，别名是shapeindex。
   35、wait：等待命令。

开发者：李兴球，微信： scratch8，电子信箱:406273900，网址 : www.lixingqiu.com，江西萍乡安源区
