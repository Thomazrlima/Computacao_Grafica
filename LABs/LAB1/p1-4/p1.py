from core.base import Base
from OpenGL.GL import*

class Janela(Base):

	def initialize(self):
		print("Initializing program...")
		glClearColor(1,0, 0.0,0.0)

	def update(self):
		glClear(GL_COLOR_BUFFER_BIT)

# instantiate this class and run the program
Janela().run()
