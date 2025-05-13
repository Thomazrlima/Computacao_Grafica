import numpy as np
import math
import pathlib
import sys

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from geometry.box import BoxGeometry
from extras.axes import AxesHelper
from extras.grid import GridHelper
from extras.movement_rig import MovementRig
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture

from core.obj_reader1 import my_obj_reader
from geometry.customGeometry import customGeometry
from geometry.custom import CustomGeometry

from geometry.rectangle import RectangleGeometry
from geometry.sphere import SphereGeometry

class Example(Base):
    """
    Render the axes and the rotated xy-grid.
    Add box and camera movement: WASDRF(move), QE(turn), TG(look).
    K changes from moving the object to moving the camera or from moving the camera to moving the object
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)

        self.object_rig = MovementRig()
        self.object_rig.set_position([0, 0.5, -0.5])

        self.object_rig2 = MovementRig()
        self.object_rig2.set_position([0, 1.5, -1.5])

        self.camera_rig = MovementRig()
        self.camera_rig.add(self.camera)
        self.camera_rig.set_position([0, 1, 2.5])
        v, uv = my_obj_reader('harmonic.obj')
        
        cima_peq_index = list(range(0, 2748))
        sphere_index = list(range(2748, 5628))
        sphere2_index = list(range(5628, 8508))
        baixo_index = list(range(8508, 8820))
        cima_index = list(range(8820, 9132))
        baix_peq_index = list(range(9132, 11880))
        sphere2_baixo_index = list(range(11880, 14760))
        sphere_baixo_index = list(range(14760, 17640))
        main_index = list(range(17640, 22200))

        cima_peq_verts = np.array([v[i] for i in cima_peq_index], dtype=np.float32)
        cima_peq_tx = np.array([uv[i] for i in cima_peq_index], dtype=np.float32)
        sphere_verts = np.array([v[i] for i in sphere_index], dtype=np.float32)
        sphere_tx = np.array([uv[i] for i in sphere_index], dtype=np.float32)
        sphere2_verts = np.array([v[i] for i in sphere2_index], dtype=np.float32)
        sphere2_tx = np.array([uv[i] for i in sphere2_index], dtype=np.float32)
        baixo_verts = np.array([v[i] for i in baixo_index], dtype=np.float32)
        baixo_tx = np.array([uv[i] for i in baixo_index], dtype=np.float32)
        cima_verts = np.array([v[i] for i in cima_index], dtype=np.float32)
        cima_tx = np.array([uv[i] for i in cima_index], dtype=np.float32)
        baixo_peq_verts = np.array([v[i] for i in baix_peq_index], dtype=np.float32)
        baixo_peq_tx = np.array([uv[i] for i in baix_peq_index], dtype=np.float32)
        sphere2_baixo_verts = np.array([v[i] for i in sphere2_baixo_index], dtype=np.float32)
        sphere2_baixo_tx = np.array([uv[i] for i in sphere2_baixo_index], dtype=np.float32)
        sphere_baixo_verts = np.array([v[i] for i in sphere_baixo_index], dtype=np.float32)
        sphere_baixo_tx = np.array([uv[i] for i in sphere_baixo_index], dtype=np.float32)
        main_verts = np.array([v[i] for i in main_index], dtype=np.float32)
        main_tx = np.array([uv[i] for i in main_index], dtype=np.float32)

        cima_peq_geometry = customGeometry(pos_d=cima_peq_verts, uv_data=cima_peq_tx)
        sphere_geometry = customGeometry(pos_d=sphere_verts, uv_data=sphere_tx)
        sphere2_geometry = customGeometry(pos_d=sphere2_verts, uv_data=sphere2_tx)
        baixo_geometry = customGeometry(pos_d=baixo_verts, uv_data=baixo_tx)
        cima_geometry = customGeometry(pos_d=cima_verts, uv_data=cima_tx)
        baixo_peq_geometry = customGeometry(pos_d=baixo_peq_verts, uv_data=baixo_peq_tx)
        sphere2_baixo_geometry = customGeometry(pos_d=sphere2_baixo_verts, uv_data=sphere2_baixo_tx)
        sphere_baixo_geometry = customGeometry(pos_d=sphere_baixo_verts, uv_data=sphere_baixo_tx)
        main_geometry = customGeometry(pos_d=main_verts, uv_data=main_tx)

        cima_peq_texture = Texture(file_name="images/metal.jpg")
        sphere_texture = Texture(file_name="images/metal.jpg")
        sphere2_texture = Texture(file_name="images/metal.jpg")
        baixo_texture = Texture(file_name="images/madeira.jpg")
        cima_texture = Texture(file_name="images/madeira.jpg")
        baixo_peq_texture = Texture(file_name="images/metal.jpg")
        sphere2_baixo_texture = Texture(file_name="images/metal.jpg")
        sphere_baixo_texture = Texture(file_name="images/metal.jpg")
        main_texture = Texture(file_name="images/metal21.jpg")

        cima_peq_material = TextureMaterial(texture=cima_peq_texture)
        sphere_material = TextureMaterial(texture=sphere_texture)
        sphere2_material = TextureMaterial(texture=sphere2_texture)
        baixo_material = TextureMaterial(texture=baixo_texture)
        cima_material = TextureMaterial(texture=cima_texture)
        baixo_peq_material = TextureMaterial(texture=baixo_peq_texture)
        sphere2_baixo_material = TextureMaterial(texture=sphere2_baixo_texture)
        sphere_baixo_material = TextureMaterial(texture=sphere_baixo_texture)
        main_material = TextureMaterial(texture=main_texture, property_dict={"repeatUV": [7, 2]})
#        main_material = TextureMaterial(texture=main_texture)

        cima_peq = Mesh(cima_peq_geometry, cima_peq_material)
        sphere = Mesh(sphere_geometry, sphere_material)
        sphere2 = Mesh(sphere2_geometry, sphere2_material)
        baixo = Mesh(baixo_geometry, baixo_material)
        cima = Mesh(cima_geometry, cima_material)
        baixo_peq = Mesh(baixo_peq_geometry, baixo_peq_material)
        sphere2_baixo = Mesh(sphere2_baixo_geometry, sphere2_baixo_material)
        sphere_baixo = Mesh(sphere_baixo_geometry, sphere_baixo_material)
        main = Mesh(main_geometry, main_material)

        self.object_rig.add(cima_peq)
        self.object_rig.add(sphere)
        self.object_rig.add(sphere2)
        self.object_rig.add(baixo)
        self.object_rig.add(cima)
        self.object_rig.add(baixo_peq)
        self.object_rig.add(sphere2_baixo)
        self.object_rig.add(sphere_baixo)
        self.object_rig.add(main)

        vertices_vermelho, texcoords_vermelho = my_obj_reader('vermelho.obj')
        vertices_branco, texcoords_branco = my_obj_reader('branco.obj')
        vertices_preto, texcoords_preto = my_obj_reader('preto.obj')
        vertices_escuro, texcoords_escuro = my_obj_reader('escuro.obj')

        escuro = Texture(file_name="images/escuro.jpg")
        vermelho = Texture(file_name="images/vermelho.jpg")
        branco = Texture(file_name="images/branco.jpg")
        preto = Texture(file_name="images/preto.jpg")

        mat_escuro = TextureMaterial(texture=escuro)
        mat_vermelho = TextureMaterial(texture=vermelho)
        mat_branco = TextureMaterial(texture=branco)
        mat_preto = TextureMaterial(texture=preto)

        geom_vermelho = customGeometry(pos_d=np.array(vertices_vermelho, dtype=np.float32),
                                    uv_data=np.array(texcoords_vermelho, dtype=np.float32))
        geom_branco = customGeometry(pos_d=np.array(vertices_branco, dtype=np.float32),
                                    uv_data=np.array(texcoords_branco, dtype=np.float32))
        geom_preto = customGeometry(pos_d=np.array(vertices_preto, dtype=np.float32),
                                    uv_data=np.array(texcoords_preto, dtype=np.float32))
        geom_escuro = customGeometry(pos_d=np.array(vertices_escuro, dtype=np.float32),
                                    uv_data=np.array(texcoords_escuro, dtype=np.float32))

        mesh_vermelho = Mesh(geom_vermelho, mat_vermelho)
        mesh_branco = Mesh(geom_branco, mat_branco)
        mesh_preto = Mesh(geom_preto, mat_preto)
        mesh_escuro = Mesh(geom_escuro, mat_escuro)

        self.object_rig2.add(mesh_vermelho)
        self.object_rig2.add(mesh_branco)
        self.object_rig2.add(mesh_preto)
        self.object_rig2.add(mesh_escuro)


        self.object_rig.rotate_y(-math.pi/2)

        self.scene.add(self.object_rig)
        self.scene.add(self.object_rig2)
        self.scene.add(self.camera_rig)

        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(texture=Texture(file_name="images/sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)
        grass_geometry = RectangleGeometry(width=100, height=100)
        grass_material = TextureMaterial(
            texture=Texture(file_name="images/Solo.jpg"),
            property_dict={"repeatUV": [50, 50]}
        )
        grass = Mesh(grass_geometry, grass_material)
        grass.rotate_x(-math.pi/2)
        self.scene.add(grass)

        self.move_camera = True
        self.input_key_states = {}
        self.control_camera = True
        self.control_object1 = False
        self.control_object2 = False
        print("Box and camera movement: WASDRF(move), QE(turn), TG(look).\nK changes from moving the object to moving the camera or from moving the camera to moving the object")

    def update(self):
        if self.input.is_key_pressed('z'):
            if not self.input_key_states.get('z', False):
                self.control_camera = True
                self.control_object1 = False
                self.control_object2 = False
            self.input_key_states['z'] = True
        elif self.input.is_key_pressed('x'):
            if not self.input_key_states.get('x', False):
                self.control_camera = False
                self.control_object1 = True
                self.control_object2 = False
            self.input_key_states['x'] = True
        elif self.input.is_key_pressed('c'):
            if not self.input_key_states.get('c', False):
                self.control_camera = False
                self.control_object1 = False
                self.control_object2 = True
            self.input_key_states['c'] = True
        else:
            self.input_key_states['z'] = False
            self.input_key_states['x'] = False
            self.input_key_states['c'] = False

        # Atualizar a entidade controlada
        if self.control_camera:
            self.camera_rig.update(self.input, self.delta_time)
        elif self.control_object1:
            self.object_rig.update(self.input, self.delta_time)
        elif self.control_object2:
            self.object_rig2.update(self.input, self.delta_time)

        # Renderizar cena
        self.renderer.render(self.scene, self.camera)

Example(screen_size=[800, 600]).run()
