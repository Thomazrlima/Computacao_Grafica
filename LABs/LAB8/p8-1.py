""" Render a basic scene that consists of a custom geometry """


from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from geometry.geometry import Geometry
from material.surface import SurfaceMaterial


class Example(Base):
    """ Render a basic scene that consists of a custom geometry """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 0.5])
        geometry = Geometry()
        p0 = [-0.1, 0.1, 0.0]
        p1 = [0.0, 0.0, 0.0]
        p2 = [0.1, 0.1, 0.0]
        p3 = [-0.2, -0.2, 0.0]
        p4 = [0.2, -0.2, 0.0]
        position_data = [p2, p3, p1, #Linha
                 p1, p3, p4,   
                 p1, p4, p0] #Linha
        geometry.add_attribute("vec3", "vertexPosition", position_data)
        R = [1, 0, 0]
        Y = [1, 1, 0]
        G = [0, 1, 0]
        B = [0, 0, 1]
        color_data = [R, G, B, B, G, R, B, R, Y]
        geometry.add_attribute("vec3", "vertexColor", color_data)
        geometry.count_vertices()
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()