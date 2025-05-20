from geometry.geometry import Geometry

class customGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1, pos_d=[], uv_data=[]):
        super().__init__()
        position_data = pos_d
        
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.count_vertices()
    
    def count_vertices(self):
        """Count the number of vertices based on the position data"""
        if hasattr(self, "attributes") and "vertexPosition" in self.attributes:
            position_data = self.attributes["vertexPosition"]["value"]
            self.vertex_count = len(position_data) // 3