import OpenGL.GL as GL
import random

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.uniform import Uniform


class Example(Base):
    """ Animate circle moving within window bounds, bouncing like a DVD logo """
    def initialize(self):
        print("Initializing program...")
        vs_code = """
            in vec3 position;
            uniform vec3 translation;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
            }
        """
        fs_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
            }
        """
        self.program_ref = Utils.initialize_program(vs_code, fs_code)

        GL.glClearColor(0.0, 0.0, 0.0, 1.0)

        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)

        position_data = self.generate_circle_vertices(0.1, 30)
        self.vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')

        self.translation = Uniform('vec3', [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')
        self.velocity = [0.01, 0.008]
    
    def generate_circle_vertices(self, radius, segments):
        import math
        vertices = [[0.0, 0.0, 0.0]]
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append([x, y, 0.0])
        return vertices

    def update(self):
        """ Update data """
        self.translation.data[0] += self.velocity[0]
        self.translation.data[1] += self.velocity[1]
        radius = 0.1

        if self.translation.data[0] + radius >= 1.0 or self.translation.data[0] - radius <= -1.0:
            self.velocity[0] *= -1
        if self.translation.data[1] + radius >= 1.0 or self.translation.data[1] - radius <= -1.0:
            self.velocity[1] *= -1
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.translation.upload_data()
        self.base_color.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, self.vertex_count)


Example().run()
