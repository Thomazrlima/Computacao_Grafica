import sys
import OpenGL.GL as GL
from core.base import Base
from core.utils import Utils
from core.attribute import Attribute

class Test(Base):
    """Move a letter 'L' with the arrow keys"""
    
    def initialize(self):
        print("Initializing program...")
        
        self.position = [0.0, 0.0]  

        vs_code = """
            in vec3 position;
            void main()
            {
                gl_Position = vec4(position, 1.0);
            }
        """
        
        # Fragment Shader
        fs_code = """
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Cor vermelha
            }
        """
        
        # Inicializando o programa de shader
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        
        if self.program_ref == 0:
            print("Shader program failed to initialize.")
            return
        
        # Definindo os vértices para formar a letra "L"
        self.vertex_data = [
            # Parte vertical do "L" (do topo até a base)
            [-0.1,  0.1,  0.0],  # Ponto superior esquerdo
            [-0.1, -0.3,  0.0],  # Ponto inferior esquerdo
            [ 0.1,  0.1,  0.0],  # Ponto superior direito

            [-0.1, -0.3,  0.0],  # Ponto inferior esquerdo
            [ 0.1, -0.3,  0.0],  # Ponto inferior direito
            [ 0.1,  0.1,  0.0],  # Ponto superior direito

            # Parte horizontal do "L" (na base)
            [-0.1, -0.3,  0.0],  # Ponto inferior esquerdo
            [-0.1, -0.5,  0.0],  # Ponto mais à esquerda na base
            [ 0.3, -0.3,  0.0],  # Ponto inferior direito

            [-0.1, -0.5,  0.0],  # Ponto mais à esquerda na base
            [ 0.3, -0.5,  0.0],  # Ponto mais à direita na base
            [ 0.3, -0.3,  0.0]   # Ponto inferior direito
        ]

        self.vertex_count = len(self.vertex_data)
        
        self.vao_L = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_L)
        
        position_attribute = Attribute('vec3', self.vertex_data)
        position_attribute.associate_variable(self.program_ref, 'position')
    
    def update(self):
        GL.glUseProgram(self.program_ref)
        GL.glBindVertexArray(self.vao_L)
        
        move_speed = 0.05
        if "up" in self.input.key_pressed_list:
            self.position[1] += move_speed  # Mover para cima
        if "down" in self.input.key_pressed_list:
            self.position[1] -= move_speed  # Mover para baixo
        if "left" in self.input.key_pressed_list:
            self.position[0] -= move_speed  # Mover para a esquerda
        if "right" in self.input.key_pressed_list:
            self.position[0] += move_speed  # Mover para a direita
        
        min_x = -1.2 + 0.3
        max_x = 1.0 - 0.3
        min_y = -1.0 + 0.5
        max_y = 1.4 - 0.5
        
        self.position[0] = max(min(self.position[0], max_x), min_x)
        self.position[1] = max(min(self.position[1], max_y), min_y)
        
        translated_vertex_data = [
            [x + self.position[0], y + self.position[1], z] for x, y, z in self.vertex_data
        ]
        
        position_attribute = Attribute('vec3', translated_vertex_data)
        position_attribute.associate_variable(self.program_ref, 'position')
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


Test().run()
