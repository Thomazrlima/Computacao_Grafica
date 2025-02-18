import OpenGL.GL as GL
import numpy as np
from core.base import Base
from core.utils import Utils
from core.attribute import Attribute

class Example(Base):
    """ Render a regular pentagon """
    def initialize(self):
        print("Initializing program...")
        vs_code = """
            in vec3 position;
            void main()
            {
                gl_Position = vec4(position.x, position.y, position.z, 1.0);
            }
        """
        fs_code = """
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 0.5, 0.0, 1.0);
            }
        """
        self.program_ref = Utils.initialize_program(vs_code, fs_code)

        GL.glLineWidth(4)

        angle = np.linspace(0, 2 * np.pi, 6)[:-1] 
        position_data_pentagon = [[np.cos(a) * 0.5, np.sin(a) * 0.5, 0.0] for a in angle]
        
        self.vertex_count_pentagon = len(position_data_pentagon)
        
        self.vao_pentagon = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_pentagon)
        
        position_attribute_pentagon = Attribute('vec3', position_data_pentagon)
        position_attribute_pentagon.associate_variable(self.program_ref, 'position')

    def update(self):
        GL.glUseProgram(self.program_ref)
        GL.glBindVertexArray(self.vao_pentagon)
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, self.vertex_count_pentagon)

Example().run()
