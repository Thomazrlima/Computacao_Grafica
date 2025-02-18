import OpenGL.GL as GL
import numpy as np
from core.base import Base
from core.utils import Utils
from core.attribute import Attribute


class Example(Base):
    """ Renderiza um hexágono preenchido com cores interpoladas """
    def initialize(self):
        print("Initializing program...")

        vs_code = """
            in vec3 position;
            in vec3 color;
            out vec3 vertexColor;
            void main()
            {
                gl_Position = vec4(position, 1.0);
                vertexColor = color; 
            }
        """

        fs_code = """
            in vec3 vertexColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(vertexColor, 1.0);
            }
        """

        self.program_ref = Utils.initialize_program(vs_code, fs_code)

        radius = 0.6
        position_data = [[0.0, 0.0, 0.0]]
        for i in range(7):
            angle = (i / 6) * (2 * np.pi)
            x = np.cos(angle) * radius
            y = np.sin(angle) * radius
            position_data.append([x, y, 0.0])

        self.vertex_count = len(position_data)

        color_data = [[1.0, 1.0, 1.0]] + [
                      [1.0, 0.0, 0.0],
                      [1.0, 1.0, 0.0],
                      [0.0, 1.0, 0.0],
                      [0.0, 1.0, 1.0],
                      [0.0, 0.0, 1.0],
                      [1.0, 0.0, 1.0],
                      [1.0, 0.0, 0.0]]

        self.vao_hexagon = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_hexagon)

        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')

        color_attribute = Attribute('vec3', color_data)
        color_attribute.associate_variable(self.program_ref, 'color')

    def update(self):
        GL.glUseProgram(self.program_ref)
        GL.glBindVertexArray(self.vao_hexagon)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, self.vertex_count)


Example().run()
