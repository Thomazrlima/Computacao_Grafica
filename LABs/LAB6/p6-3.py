import math
import random
import sys
from math import pi
import OpenGL.GL as GL

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from core.obj_reader import my_obj_reader

class Example(Base):
    """
    Move a triangle around the screen: global and local transformations.
    Use keys w, a, s ,d, z, x, q, e and i, j, k ,l, u, p, respectively.
    """
    def initialize(self):
        """Setup the object and shaders"""
        print('Initializing program...')
        ### Initialize program ###
        vs_code = """
                   in vec3 position;
                   uniform mat4 projectionMatrix;
                   uniform mat4 modelMatrix;
                   in vec3 vertexColor;
                   out vec3 baseColor;
                   void main()
                   {
                       gl_Position = projectionMatrix * modelMatrix * vec4(position, 4.0);
                       baseColor = vertexColor;
                   }
               """
        fs_code = """
                   in vec3 baseColor;
                   out vec4 fragColor;
                   void main()
                   {
                       fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
                   }
               """
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        ### Render settings ###
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        ### Set up vertex array object ###
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        ### Set up vertex attribute: three points of triangle ###
        position_data = my_obj_reader('untitled.obj')
        color_data = [[1.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0],
                      [0.0, 0.0, 1.0],
                      [0.6, 0.2, 0.8],
                      [1.0, 1.0, 0.0],
                      [1.0, 0.55, 0.0],
                      [1.0, 0.8, 0.86],
                      [0.59, 0.29, 0.0]]
        self.vertex_count = len(position_data)
        for i in range(len(position_data) - 8):
            color_data.append([random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)])

        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')
        ### Set up uniforms ###
        m_matrix = Matrix.make_translation(0, 0, -1)
        self.model_matrix = Uniform('mat4', m_matrix)
        self.model_matrix.locate_variable(self.program_ref, 'modelMatrix')
        p_matrix = Matrix.make_perspective()
        self.projection_matrix = Uniform('mat4', p_matrix)
        self.projection_matrix.locate_variable(self.program_ref, 'projectionMatrix')
        color_attribute = Attribute("vec3", color_data)
        color_attribute.associate_variable(self.program_ref, 'vertexColor')
        # movement speed, units per second
        self.move_speed = 0.5
        # rotation speed, radians per second
        self.turn_speed = 90 * (pi / 180)

    def update(self):
        """ Update data """
        move_amount = self.move_speed * self.delta_time
        turn_amount = self.turn_speed * self.delta_time
        # global translation
        if self.input.is_key_pressed('w'):
            m = Matrix.make_translation(0, move_amount, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed('s'):
            m = Matrix.make_translation(0, -move_amount, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed('a'):
            m = Matrix.make_translation(-move_amount, 0, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed('d'):
            m = Matrix.make_translation(move_amount, 0, 0)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed('z'):
            m = Matrix.make_translation(0, 0, move_amount)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed('x'):
            m = Matrix.make_translation(0, 0, -move_amount)
            self.model_matrix.data = m @ self.model_matrix.data
        # global rotation (around the origin)
        if self.input.is_key_pressed('q'):
            m = Matrix.make_rotation_z(turn_amount)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_pressed('e'):
            m = Matrix.make_rotation_z(-turn_amount)
            self.model_matrix.data = m @ self.model_matrix.data
        # local translation
        if self.input.is_key_pressed('i'):
            m = Matrix.make_translation(0, move_amount, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed('k'):
            m = Matrix.make_translation(0, -move_amount, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed('j'):
            m = Matrix.make_translation(-move_amount, 0, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed('l'):
            m = Matrix.make_translation(move_amount, 0, 0)
            self.model_matrix.data = self.model_matrix.data @ m
        # local rotation (around object center)
        if self.input.is_key_pressed('u'):
            m = Matrix.make_rotation_z(turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed('o'):
            m = Matrix.make_rotation_z(-turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m

        if self.input.is_key_down('b'):
            m = Matrix.make_scalex(-1)
            self.model_matrix.data = m @ self.model_matrix.data
        if self.input.is_key_down('c'):
            m = Matrix.make_scaley(-1)
            self.model_matrix.data = m @ self.model_matrix.data

        if self.input.is_key_pressed('right'):
            m = Matrix.make_rotation_y(turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed('left'):
            m = Matrix.make_rotation_y(-turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed('up'):
            m = Matrix.make_rotation_x(-turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m
        if self.input.is_key_pressed('down'):
            m = Matrix.make_rotation_x(turn_amount)
            self.model_matrix.data = self.model_matrix.data @ m
        ### Render scene ###
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.projection_matrix.upload_data()
        self.model_matrix.upload_data()
        #GL.glDrawArrays(GL.GL_LINE_LOOP, 0, self.vertex_count)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


# Instantiate this class and run the program
Example().run()