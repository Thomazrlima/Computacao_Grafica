import math
import OpenGL.GL as GL

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.uniform import Uniform


class Example(Base):
    """ Animate triangle moving in a circular path around the origin """
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

        position_data = [[ 0.0,  0.2,  0.0],
                         [ 0.2, -0.2,  0.0],
                         [-0.2, -0.2,  0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')
        
        # Set up uniforms #
        self.translation = Uniform('vec3', [-0.5, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')

    def update(self):
        """ Update data """
        self.translation.data[0] = 0.75 * math.cos(self.time)
        self.translation.data[1] = 0.75 * math.sin(self.time)
   
        self.base_color.data[0] = (math.sin(self.time) + 1) / 2  # R
        self.base_color.data[1] = (math.sin(self.time + 2) + 1) / 2  # G
        self.base_color.data[2] = (math.sin(self.time + 4) + 1) / 2  # B
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.translation.upload_data()
        self.base_color.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

Example().run()
