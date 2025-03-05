import math
import random
import OpenGL.GL as GL

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.uniform import Uniform


class Example(Base):
    """ Animate triangle appearing and disappearing at random positions """
    def initialize(self):
        print("Initializing program...")
        vs_code = """
            in vec3 position;
            uniform vec3 translation;
            uniform float alpha;
            out float vAlpha;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
                vAlpha = alpha;
            }
        """
        fs_code = """
            uniform vec3 baseColor;
            in float vAlpha;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, vAlpha);
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
    
        self.translation = Uniform('vec3', [0.0, 0.0, 0.0])
        self.translation.locate_variable(self.program_ref, 'translation')
        self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color.locate_variable(self.program_ref, 'baseColor')
        self.alpha = Uniform('float', 1.0)
        self.alpha.locate_variable(self.program_ref, 'alpha')

        self.next_position_time = 0

    def update(self):
        """ Update data """
        if self.time >= self.next_position_time:
            self.translation.data[0] = random.uniform(-0.8, 0.8)
            self.translation.data[1] = random.uniform(-0.8, 0.8)
            self.next_position_time = self.time + 1.6

        self.base_color.data[0] = (math.sin(self.time * 3) + 1) / 2
        
        self.alpha.data = (math.sin(self.time * 2) + 1) / 2

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.program_ref)
        self.translation.upload_data()
        self.base_color.upload_data()
        self.alpha.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Example().run()
