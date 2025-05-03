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
from extras.movement_rig2 import MovementRig
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
    Renderiza os eixos, uma grade girada no eixo XY e carrega objetos de arquivos .obj.
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0.5, 1, 5])

        self.mesh = {}

        # Carregar modelo vermelho
        vertices_red, text_cords_red = my_obj_reader('vermelho.obj')
        geometry_red = customGeometry(1, 1, 1, vertices_red, text_cords_red)
        texture_red = Texture(file_name="images/vermelho.jpg")
        material_red = TextureMaterial(texture=texture_red)
        self.mesh["red"] = Mesh(geometry_red, material_red)

        # Carregar modelo preto
        vertices_black, text_cords_black = my_obj_reader('preto.obj')
        geometry_black = customGeometry(1, 1, 1, vertices_black, text_cords_black)
        texture_black = Texture(file_name="images/preto.jpg")
        material_black = TextureMaterial(texture=texture_black)
        self.mesh["black"] = Mesh(geometry_black, material_black)

        # Carregar modelo branco
        vertices_white, text_cords_white = my_obj_reader('branco.obj')
        geometry_white = customGeometry(1, 1, 1, vertices_white, text_cords_white)
        texture_white = Texture(file_name="images/branco.jpg")
        material_white = TextureMaterial(texture=texture_white)
        self.mesh["white"] = Mesh(geometry_white, material_white)
        
        # Carregar modelo escuro
        vertices_dark, text_cords_dark = my_obj_reader('Escuro.obj')
        geometry_dark = customGeometry(1, 1, 1, vertices_dark, text_cords_dark)
        texture_dark = Texture(file_name="images/escuro.jpg")
        material_dark = TextureMaterial(texture=texture_dark)
        self.mesh["dark"] = Mesh(geometry_dark, material_dark)
    
        # Criando o MovementRig e passando um valor numérico para units_per_second
        self.rig = MovementRig(units_per_second=1)  # Corrigido para passar um valor numérico
        self.rig.add(self.mesh["red"])
        self.rig.add(self.mesh["black"])
        self.rig.add(self.mesh["white"])
        self.rig.add(self.mesh["dark"])
        
        self.scene.add(self.rig)
        
        # Adicionar eixos e grade
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
