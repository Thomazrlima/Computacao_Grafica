import OpenGL.GL as GL

from core.base import Base
from core.utils import Utils
from core.attribute import Attribute
from core.uniform import Uniform


class Example(Base):
    """ Render four triangles positioned as a Triforce and one separate """

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
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        position_data = [[ 0.0,  0.2,  0.0],
                         [ 0.2, -0.2,  0.0],
                         [-0.2, -0.2,  0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')
        self.triangles = [
            {'translation': Uniform('vec3', [-0.2,  0.0, 0.0]), 'color': Uniform('vec3', [1.0, 0.0, 0.0])},
            {'translation': Uniform('vec3', [ 0.2,  0.0, 0.0]), 'color': Uniform('vec3', [0.0, 0.0, 1.0])},
            {'translation': Uniform('vec3', [ 0.0, 0.4, 0.0]), 'color': Uniform('vec3', [0.0, 1.0, 0.0])},
            {'translation': Uniform('vec3', [ 0.6, -0.4, 0.0]), 'color': Uniform('vec3', [1.0, 1.0, 0.0])}  # Separate triangle
        ]
        for triangle in self.triangles:
            triangle['translation'].locate_variable(self.program_ref, 'translation')
            triangle['color'].locate_variable(self.program_ref, 'baseColor')

    def update(self):
        GL.glUseProgram(self.program_ref)
        for triangle in self.triangles:
            triangle['translation'].upload_data()
            triangle['color'].upload_data()
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)

Example().run()
