from materials.basic_material import BasicMaterial
from materials.blinn_phong_material import BlinnPhongMaterial
from materials.fresnel_material import FresnelMaterial
from object.object import Object
from object.triangle import Triangle
from pyglm import glm
class Model():

    def __init__(self, vertices, faces, mat):
        self.vertices = vertices
        self.faces = faces
        self.triangles = []
        self.mat = mat

    def generate_triangles(self):
        list_of_triangles = []
        for f in self.faces:
            v0 = self.vertices[f[0]]
            v1 = self.vertices[f[1]]
            v2 = self.vertices[f[2]]
            triangle = Triangle(v0, v1, v2, FresnelMaterial(refract_index=1.33,color=[1.0, 1.0, 1.0]))
            list_of_triangles.append(triangle)
        self.triangles =  list_of_triangles
    def barycentre(self):
        barycentre = glm.vec3(0.0)
        for v in self.vertices:
            barycentre += v
        barycentre /= len(self.vertices)
        return barycentre
    def translate(self, translation_vector):
        for i in range(len(self.vertices)):
            self.vertices[i] += translation_vector
    
    def scale(self, scale_factor):
        for i in range(len(self.vertices)):
            self.vertices[i] *= scale_factor
    
    def scale_uniform(self, scale_factor, center=None):
        """
        Scale uniformément le modèle.
        - scale_factor: scalaire ou glm.vec3 (si scalaire, uniforme).
        - center: glm.vec3 optionnel, point autour duquel scaler. Par défaut le barycentre.
        """
        # normaliser scale_factor en vec3
        if isinstance(scale_factor, (int, float)):
            s = glm.vec3(float(scale_factor), float(scale_factor), float(scale_factor))
        else:
            s = glm.vec3(scale_factor)

        if center is None:
            center = self.barycentre()
        else:
            center = glm.vec3(center)

        for i in range(len(self.vertices)):
            v = glm.vec3(self.vertices[i])
            # translation au centre, scale, puis retour
            self.vertices[i] = center + (v - center) * s
    
    def rotate_y(self, angle_in_degrees, center=None):
        """
        Rotate le modèle autour de l'axe Y.
        - angle_in_degrees: angle en degrés.
        - center: glm.vec3 optionnel, point autour duquel tourner. Par défaut le barycentre.
        """
        angle_in_radians = glm.radians(angle_in_degrees)
        rotation_matrix = glm.mat3(
            glm.cos(angle_in_radians), 0, glm.sin(angle_in_radians),
            0, 1, 0,
            -glm.sin(angle_in_radians), 0, glm.cos(angle_in_radians)
        )

        if center is None:
            center = self.barycentre()
        else:
            center = glm.vec3(center)

        for i in range(len(self.vertices)):
            v = glm.vec3(self.vertices[i])
            # translation au centre, rotation, puis retour
            self.vertices[i] = center + rotation_matrix * (v - center)