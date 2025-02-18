import OpenGL.GL as GL
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
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 0.0, 0.0, 1.0);
            }
        """

        self.program_ref = Utils.initialize_program(vs_code, fs_code)

        position_data = [
            [-0.6,  0.6,  0.0],
            [-0.4,  0.6,  0.0],
            [-0.6, -0.6,  0.0],

            [-0.6, -0.6,  0.0],
            [-0.4,  0.6,  0.0],
            [-0.4, -0.6,  0.0],

            [-0.6, -0.6,  0.0],
            [ 0.4, -0.6,  0.0],
            [-0.6, -0.4,  0.0],

            [-0.6, -0.4,  0.0],
            [ 0.4, -0.6,  0.0],
            [ 0.4, -0.4,  0.0]
        ]

        self.vertex_count = len(position_data)

        self.vao_L = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_L)

        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')

    def update(self):
        GL.glUseProgram(self.program_ref)
        GL.glBindVertexArray(self.vao_L)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Example().run()
