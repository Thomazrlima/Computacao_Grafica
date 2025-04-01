import numpy as np
import math
import pathlib
import sys
import os

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
from core_ext.texture import Texture
from material.texture import TextureMaterial
import OpenGL.GL as GL

class SurfaceMaterialWithTexture(SurfaceMaterial):
    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, property_dict={}, use_vertex_colors=True):
        super().__init__(vertex_shader_code, fragment_shader_code, property_dict, use_vertex_colors)
        self.texture = None

    def set_texture(self, texture):
        """Método para configurar a textura no material."""
        self.texture = texture
        self._setting_dict["useTexture"] = True

    def update_render_settings(self):
        """Atualiza as configurações de renderização."""
        super().update_render_settings()
        if self.texture:
            GL.glActiveTexture(GL.GL_TEXTURE0)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.texture_ref)  
class Example(Base):
    """
    Render the axes and the rotated xy-grid.
    Import and display an object from the .obj file.
    Add movement: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        print("Para mexer a câmera use as teclas ↑, ↓, ←, →")
        self.renderer = Renderer()
        self.scene = Scene()
        
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0.5, 1, 5])
        
        vertices_red, text_cords_red = my_obj_reader('vermelho.obj')
        geometry_red = customGeometry(1, 1, 1, vertices_red, text_cords_red)
        texture_red = Texture(file_name="images/vermelho.jpg")
        material_red = TextureMaterial(texture= texture_red)

        self.mesh = Mesh(geometry_red, material_red)

        vertices_black, text_cords_black = my_obj_reader('preto.obj')
        geometry_black = customGeometry(1, 1, 1, vertices_black, text_cords_black)
        texture_black = Texture(file_name="images/preto.jpg")
        material_black = TextureMaterial(texture= texture_black)

        self.mesh.black = Mesh(geometry_black, material_black)

        vertices_white, text_cords_white = my_obj_reader('branco.obj')
        geometry_white = customGeometry(1, 1, 1, vertices_white, text_cords_white)
        texture_white = Texture(file_name="images/branco.jpg")
        material_white = TextureMaterial(texture= texture_white)

        self.mesh.white = Mesh(geometry_white, material_white)
        
        vertices_dark, text_cords_dark = my_obj_reader('Escuro.obj')
        geometry_dark = customGeometry(1, 1, 1, vertices_dark, text_cords_dark)
        texture_dark = Texture(file_name="images/escuro.jpg")
        material_dark = TextureMaterial(texture= texture_dark)

        self.mesh.dark = Mesh(geometry_dark, material_dark)
    
        self.rig = MovementRig(self.camera)
        self.rig.add(self.mesh)
        self.mesh.add(self.mesh.black)
        self.mesh.add(self.mesh.white)
        self.mesh.add(self.mesh.dark)
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
