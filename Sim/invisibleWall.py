import pymunk


class InvisibleWall:

    def __init__(self, x, y, xSize, ySize):
        self.x = x
        self.y = y
        self.xSize = xSize
        self.ySize = ySize
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (self.x, self.y)
        self.shape = pymunk.Poly.create_box(self.body, size=(self.xSize, self.ySize))