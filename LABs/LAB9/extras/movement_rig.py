import math
from core_ext.object3d import Object3D

class MovementRig(Object3D):
    def __init__(self, camera, units_per_second=1, degrees_per_second=60):
        super().__init__()
        self._look_attachment = Object3D()
        self.children_list = [self._look_attachment]
        self._look_attachment.parent = self
        self._units_per_second = units_per_second
        self._degrees_per_second = degrees_per_second

        # Inicializando a rotação para evitar erro
        self.rotation = [0.0, 0.0, 0.0]
        self.camera = camera  

        # Mapeamento de teclas
        self.KEY_MOVE_FORWARDS = ["w"]
        self.KEY_MOVE_BACKWARDS = ["s"]
        self.KEY_MOVE_LEFT = ["a"]
        self.KEY_MOVE_RIGHT = ["d"]
        self.KEY_MOVE_UP = ["r"]
        self.KEY_MOVE_DOWN = ["f"]
        self.KEY_TURN_LEFT = ["q"]
        self.KEY_TURN_RIGHT = ["e"]
        self.KEY_LOOK_UP = ["t"]
        self.KEY_LOOK_DOWN = ["g"]

        # Setas movem a câmera
        self.KEY_CAM_MOVE_LEFT = ["left"]
        self.KEY_CAM_MOVE_RIGHT = ["right"]
        self.KEY_CAM_MOVE_UP = ["up"]
        self.KEY_CAM_MOVE_DOWN = ["down"]

    def add(self, child):
        self._look_attachment.add(child)

    def remove(self, child):
        self._look_attachment.remove(child)

    def update(self, input_object, delta_time):
        move_amount = self._units_per_second * delta_time
        rotate_amount = self._degrees_per_second * (math.pi / 180) * delta_time
        
        # Cálculo de direção
        cos_r = math.cos(self.rotation[1])
        sin_r = math.sin(self.rotation[1])
        forward = [sin_r * move_amount, 0, cos_r * move_amount]
        right = [cos_r * move_amount, 0, -sin_r * move_amount]

        # Movimento do objeto com WASD
        if any(input_object.is_key_pressed(k) for k in self.KEY_MOVE_FORWARDS):
            self.translate(-forward[0], 0, -forward[2])
        if any(input_object.is_key_pressed(k) for k in self.KEY_MOVE_BACKWARDS):
            self.translate(forward[0], 0, forward[2])
        if any(input_object.is_key_pressed(k) for k in self.KEY_MOVE_LEFT):
            self.translate(-right[0], 0, -right[2])
        if any(input_object.is_key_pressed(k) for k in self.KEY_MOVE_RIGHT):
            self.translate(right[0], 0, right[2])
        if any(input_object.is_key_pressed(k) for k in self.KEY_MOVE_UP):
            self.translate(0, move_amount, 0)
        if any(input_object.is_key_pressed(k) for k in self.KEY_MOVE_DOWN):
            self.translate(0, -move_amount, 0)

        # Rotação do objeto
        if any(input_object.is_key_pressed(k) for k in self.KEY_TURN_RIGHT):
            self.rotate_y(-rotate_amount)
            self.rotation[1] -= rotate_amount  
        if any(input_object.is_key_pressed(k) for k in self.KEY_TURN_LEFT):
            self.rotate_y(rotate_amount)
            self.rotation[1] += rotate_amount  

        if any(input_object.is_key_pressed(k) for k in self.KEY_LOOK_UP):
            self._look_attachment.rotate_x(rotate_amount)
        if any(input_object.is_key_pressed(k) for k in self.KEY_LOOK_DOWN):
            self._look_attachment.rotate_x(-rotate_amount)

        # Movimento da câmera com setas
        if any(input_object.is_key_pressed(k) for k in self.KEY_CAM_MOVE_LEFT):
            self.camera.translate(-move_amount, 0, 0)
        if any(input_object.is_key_pressed(k) for k in self.KEY_CAM_MOVE_RIGHT):
            self.camera.translate(move_amount, 0, 0)
        if any(input_object.is_key_pressed(k) for k in self.KEY_CAM_MOVE_UP):
            self.camera.translate(0, move_amount, 0)
        if any(input_object.is_key_pressed(k) for k in self.KEY_CAM_MOVE_DOWN):
            self.camera.translate(0, -move_amount, 0)
