from pyglm import glm

class Light:
    position = glm.vec3(0.0,0.0,0.0)
    color = glm.vec3(1.0,1.0,1.0)

    def __init__(self, position, color):
        self.position = position
        self.color = color

    def getPosition(self):
        return self.position
    
    def getColor(self):
        return self.color

    