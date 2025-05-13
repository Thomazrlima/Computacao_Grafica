import sys

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.texture import Texture
from geometry.polygon import PolygonGeometry
from material.material import Material


class Example(Base):
    """
    Blend between two different textures cyclically.  The fragment shader
    samples colors from two textures at each fragment, and then, linearly
    interpolates between these colors to determine the output fragment color.
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=500/500)
        self.camera.set_position([0, 0, 1.5])
        vertex_shader_code = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            out vec2 UV;

            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 2.0)+0.5;
                UV = vertexUV;
            }
        """
        fragment_shader_code = """
            uniform sampler2D texture1;
            uniform sampler2D texture2;
            uniform sampler2D texture;
            in vec2 UV;
            uniform float time;
            out vec4 fragColor;

            void main()
            {
                vec2 stretchedUV = UV * vec2(1, 2.0);
                vec2 shiftUV = stretchedUV + vec2(0, 0.2 * sin(6.0 * stretchedUV.x + time));
                fragColor = texture2D(texture, shiftUV);
                vec4 color1 = texture2D(texture1, shiftUV);
                vec4 color2 = texture2D(texture2, shiftUV);
                float s = abs(sin(time));
                fragColor = s * color1 + (1.0 - s) * color2;
            }
        """
        grid_texture = Texture("images/Magrao.jpg")
        crate_texture = Texture("images/CR7Real.jpeg")
        self.blend_material = Material(vertex_shader_code, fragment_shader_code)
        self.blend_material.add_uniform("sampler2D", "texture1", [grid_texture.texture_ref, 1])
        self.blend_material.add_uniform("sampler2D", "texture2", [crate_texture.texture_ref, 2])
        self.blend_material.add_uniform("float", "time", 0.0)
        self.blend_material.locate_uniforms()

        geometry = PolygonGeometry()
        self.mesh = Mesh(geometry, self.blend_material)
        self.scene.add(self.mesh)

    def update(self):
        self.blend_material.uniform_dict["time"].data += self.delta_time
        self.renderer.render(self.scene, self.camera)


Example(screen_size=[800, 600]).run()
