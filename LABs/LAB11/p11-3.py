import math

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.texture import Texture
from geometry.rectangle import RectangleGeometry
from geometry.sphere import SphereGeometry
from material.texture import TextureMaterial
from extras.movement_rig import MovementRig
from material.material import Material


class Example(Base):
    """
    Render a textured skysphere and a textured grass floor.
    Add camera movement: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([0, 1, 4])
        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(texture=Texture(file_name="images/sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)
        grass_geometry = RectangleGeometry(width=100, height=100)
        grass_material = TextureMaterial(
            texture=Texture(file_name="images/grass.jpg"),
            property_dict={"repeatUV": [50, 50]}
        )
        grass = Mesh(grass_geometry, grass_material)
        grass.rotate_x(-math.pi/2)
        self.scene.add(grass)
        geometry = SphereGeometry()

        vertex_shader_code = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            out vec2 UV;
            
            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                UV = vertexUV;
            }
        """
        fragment_shader_code = """
            uniform sampler2D texture;
            in vec2 UV;
            uniform float time;
            out vec4 fragColor;
            
            void main()
            {
                vec2 shiftUV = UV + vec2(0, 0.2 * sin(6.0 * UV.x + time));
                fragColor = texture2D(texture, shiftUV);
            }
        """
        grid_texure = Texture("images/Emoji.png")
        self.wave_material = Material(vertex_shader_code, fragment_shader_code)
        self.wave_material.add_uniform("sampler2D", "texture", [grid_texure.texture_ref, 1])
        self.wave_material.add_uniform("float", "time", 0.0)
        self.wave_material.locate_uniforms()
        self.mesh = Mesh(geometry, self.wave_material)
        self.scene.add(self.mesh)
        self.mesh.translate(0,1,0)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
