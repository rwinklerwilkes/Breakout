__author__ = 'Rich'

class Shape:
    def __init__(self,x_cor,y_cor,width,height,img):
        self.x = x_cor
        self.y = y_cor
        self.width = width
        self.height = height
        self.img = img

class Ball(Shape):
    def __init__(self,x_cor,y_cor,width,height,img,speed):
        super().__init__(x_cor,y_cor,width,height,img)
        self.speed = speed

class Block(Shape):
    def __init__(self,x_cor,y_cor,width,height,img,alive = True):
        super().__init__(x_cor,y_cor,width,height,img)
        self.alive = alive