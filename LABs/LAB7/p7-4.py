"""An example of a basic scene: spinning cube"""

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from geometry.box import BoxGeometry
from material.surface import SurfaceMaterial
from core.obj_reader import my_obj_reader
from material.point import PointMaterial
from core.customGeometry import customGeometry


class Example(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 4])
        
        geometry = customGeometry(1, 1, 1, my_obj_reader('untitled.obj'))
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)
        
        self.rotation_speed = 0.0
        self.rotate_x = False
        self.rotate_y = False
        self.rotate_z = False
        
    def update(self):
        if self.rotate_x:
            self.mesh.rotate_x(self.rotation_speed)
        if self.rotate_y:
            self.mesh.rotate_y(self.rotation_speed)
        if self.rotate_z:
            self.mesh.rotate_z(self.rotation_speed)
        
        self.renderer.render(self.scene, self.camera)
        
        if self.input.is_key_pressed('s'):
            self.rotation_speed = 0.005
        if self.input.is_key_pressed('f'):
            self.rotation_speed = 0.05
        if self.input.is_key_pressed('p'):
            self.rotation_speed = False
        if self.input.is_key_pressed('x'):
            self.rotate_x = not self.rotate_x
        if self.input.is_key_pressed('y'):
            self.rotate_y = not self.rotate_y
        if self.input.is_key_pressed('z'):
            self.rotate_z = not self.rotate_z
        
        # Se ativar alguma rotação, garantir que a velocidade não seja zero
        if self.rotate_x or self.rotate_y or self.rotate_z:
            if self.rotation_speed == 0.0:
                self.rotation_speed = 0.02

Example(screen_size=[800, 600]).run()
