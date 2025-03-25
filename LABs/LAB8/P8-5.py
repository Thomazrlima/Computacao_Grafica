import numpy as np
import math
import pathlib
import sys

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from extras.axes import AxesHelper
from extras.grid import GridHelper
from extras.movement_rig import MovementRig
from material.surface import SurfaceMaterial
from core.obj_reader import my_obj_reader  
from core.customGeometry import customGeometry  

class Example(Base):
    """
    Render the axes and the rotated xy-grid.
    Import and display an object from the .obj file.
    Add movement: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0.5, 1, 5])
        
        geometry = customGeometry(1, 1, 1, my_obj_reader('untitled.obj'))
        
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        
        self.mesh = Mesh(geometry, material)
        
        self.rig = MovementRig()
        self.rig.add(self.mesh)
        self.rig.set_position([0, 0.5, -0.5])
        
        self.scene.add(self.rig)
        
        axes = AxesHelper(axis_length=2)
        self.scene.add(axes)
        
        grid = GridHelper(
            size=20,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        
        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()
