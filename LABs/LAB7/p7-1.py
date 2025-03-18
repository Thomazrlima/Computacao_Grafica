from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from geometry.box import BoxGeometry
from material.surface import SurfaceMaterial
import numpy as np


class Example(Base):
    """ Render a basic scene that consists of a spinning cube """
    def initialize(self):
            print("Initializing program...")
            self.renderer = Renderer()
            self.scene = Scene()
            self.camera = Camera(aspect_ratio=800/600)
            self.camera.set_position([0.5, -0.5, 3])
            geometry = BoxGeometry()
            #material = PointMaterial(property_dict={"baseColor": [1, 1, 0], "pointSize": 5})
            #material = SurfaceMaterial(property_dict={"useVertexColors": False})
            material = SurfaceMaterial(
                property_dict= {
                    "useVertexColors": True,
                    "wireframe": True,
                    "lineWidth": 8,
                    "doubleSide": True
                }
            )
            self.mesh = Mesh(geometry, material)
            self.scene.add(self.mesh)

    def update(self):
        self.mesh.rotate_y(0.02514)
        self.mesh.rotate_x(0.01337)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
