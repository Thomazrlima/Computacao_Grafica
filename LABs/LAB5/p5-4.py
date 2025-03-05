import OpenGL.GL as GL
import math
import time
import random
from core.base import Base
from core.utils import Utils
from core.attribute import Attribute

class Example(Base):
    def initialize(self):
        print("Initializing program...")

        vs_code = """
            in vec3 position;
            void main()
            {
                gl_Position = vec4(position, 1.0);
            }
        """

        fs_code = """
            uniform float time;
            uniform vec3 color;
            out vec4 fragColor;
            void main()
            {
                // Controle do fade-in: a cor começa invisível e se torna visível ao longo do tempo
                float alpha = mod(time, 2.0) < 1.0 ? mod(time, 1.0) : 1.0;  // Fade-in de 0 a 1 e depois se mantém 1
                
                // A cor do triângulo
                fragColor = vec4(color.r, color.g, color.b, alpha);
            }
        """

        self.program_ref = Utils.initialize_program(vs_code, fs_code)

        if self.program_ref == 0:
            print("Shader program failed to initialize.")
            return

        self.vertex_data = [
            [-0.1,  0.1,  0.0], [-0.1, -0.3,  0.0], [ 0.1,  0.1,  0.0],
            [-0.1, -0.3,  0.0], [ 0.1, -0.3,  0.0], [ 0.1,  0.1,  0.0],
            [-0.1, -0.3,  0.0], [-0.1, -0.5,  0.0], [ 0.3, -0.3,  0.0],
            [-0.1, -0.5,  0.0], [ 0.3, -0.5,  0.0], [ 0.3, -0.3,  0.0]
        ]

        self.vertex_count = len(self.vertex_data)

        self.vao_L = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_L)

        position_attribute = Attribute('vec3', self.vertex_data)
        position_attribute.associate_variable(self.program_ref, 'position')

        self.start_time = time.time()
        
        self.random_color = [random.random(), random.random(), random.random()]
        
        self.final_color = [0.0, 0.0, 1.0]

    def update(self):
        GL.glUseProgram(self.program_ref)
        GL.glBindVertexArray(self.vao_L)

        current_time = time.time() - self.start_time
        time_location = GL.glGetUniformLocation(self.program_ref, 'time')
        GL.glUniform1f(time_location, current_time)

        if current_time < 1:
            color_location = GL.glGetUniformLocation(self.program_ref, 'color')
            GL.glUniform3fv(color_location, 1, self.random_color)
        else:
            color_location = GL.glGetUniformLocation(self.program_ref, 'color')
            GL.glUniform3fv(color_location, 1, self.final_color)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

        if current_time > 0.5:
            self.random_color = [0.0,0.0,0.0]

        if current_time > 1:
            self.random_color = [random.random(), random.random(), random.random()]
            self.start_time = time.time()

Example().run()
