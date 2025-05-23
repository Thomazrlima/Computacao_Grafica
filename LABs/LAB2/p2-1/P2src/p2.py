"""Apresenta um ponto na janela"""
from OpenGL import GL

from core.base import Base
from core.utils import Utils


class Example(Base):
    """Renderiza um único ponto"""
    def initialize(self):
        print("Initializing program...")
        # Initialize program #
        # vertex shader code
        vs_code = """
            void main()
            {
                gl_Position = vec4(0.2, 0.3, 0.0, 1.0);
            }
        """
        # fragment shader code
        fs_code = """
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 0.0, 0.0, 1.0);
            }
        """
        # Send code to GPU and compile; store program reference
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        # Set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # render settings (optional) #
        # Set point width and height
        GL.glPointSize(200)

    def update(self):
        """Seleciona programa a executar na GPU e apresenta os resultado do GPU"""
        # Select program to use when rendering
        GL.glUseProgram(self.program_ref)
        # Renders geometric objects using selected program
        GL.glDrawArrays(GL.GL_POINTS, 0, 1)


# Instantiate this class and run the program
Example().run()
