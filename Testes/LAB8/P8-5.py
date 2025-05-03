import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time
import json
import struct
from OpenGL.GLUT import glutInit, glutSolidCube
import os

class GLTFLoader:
    def __init__(self):
        self.vaos = []
        self.textures = []
        self.nodes = []
        self.animations = []
        self.current_animation = None
        self.animation_start_time = 0
        self.buffers = []  # Adicionado para armazenar buffers

    def load_gltf(self, file_path):
        if file_path.endswith('.glb'):
            self.load_glb(file_path)
        else:
            self.load_gltf_json(file_path)

    def load_glb(self, file_path):
        with open(file_path, 'rb') as f:
            # Ler cabeçalho GLB
            magic = f.read(4)
            version = struct.unpack('<I', f.read(4))[0]
            length = struct.unpack('<I', f.read(4))[0]
            
            # Ler chunk JSON
            chunk_length = struct.unpack('<I', f.read(4))[0]
            chunk_type = f.read(4)
            json_data = json.loads(f.read(chunk_length).decode('utf-8'))
            
            # Ler chunk BIN
            chunk_length = struct.unpack('<I', f.read(4))[0]
            chunk_type = f.read(4)
            bin_data = f.read(chunk_length)
            
            self.process_gltf_data(json_data, bin_data)

    def load_gltf_json(self, file_path):
        dir_path = os.path.dirname(os.path.abspath(file_path))
        
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        
        # Corrigir caminhos dos buffers
        if 'buffers' in json_data:
            for buffer in json_data['buffers']:
                if 'uri' in buffer and not buffer['uri'].startswith('data:'):
                    buffer_path = os.path.join(dir_path, buffer['uri'])
                    if not os.path.exists(buffer_path):
                        raise FileNotFoundError(f"Arquivo binário não encontrado: {buffer_path}")
                    buffer['uri'] = buffer_path
        
        self.process_gltf_data(json_data, None)

    def process_buffers(self):
        """Processa todos os buffers do arquivo glTF"""
        if 'buffers' not in self.json_data:
            return
            
        self.buffers = []
        for buffer in self.json_data['buffers']:
            if buffer.get('uri', '').startswith('data:'):
                # Implementar se necessário para URIs data:
                pass
            elif self.bin_data:
                # Usar dados binários do GLB
                self.buffers.append(self.bin_data)
            else:
                # Carregar de arquivo externo (glTF separado)
                with open(buffer['uri'], 'rb') as f:
                    self.buffers.append(f.read())

    def process_gltf_data(self, data, bin_data):
        self.json_data = data
        self.bin_data = bin_data
        
        # Processar buffers (agora este método existe)
        self.process_buffers()
        
        # Processar nós
        if 'nodes' in data:
            for node in data['nodes']:
                self.process_node(node)
        
        # Processar animações
        if 'animations' in data:
            for anim in data['animations']:
                self.process_animation(anim)
        
        # Processar cena
        if 'scenes' in data:
            scene = data['scenes'][data.get('scene', 0)]
            for node_idx in scene.get('nodes', []):
                if node_idx < len(self.nodes):
                    self.nodes[node_idx]['is_root'] = True

    def process_node(self, node_data):
        node = {
            'name': node_data.get('name', ''),
            'mesh': node_data.get('mesh', None),
            'translation': np.array(node_data.get('translation', [0, 0, 0])),
            'rotation': np.array(node_data.get('rotation', [0, 0, 0, 1])),
            'scale': np.array(node_data.get('scale', [1, 1, 1])),
            'children': node_data.get('children', []),
            'matrix': np.array(node_data.get('matrix', np.identity(4))),
            'is_root': False
        }
        self.nodes.append(node)

    def process_animation(self, anim_data):
        animation = {
            'name': anim_data.get('name', 'unnamed'),
            'channels': [],
            'samplers': []
        }
        
        for channel in anim_data.get('channels', []):
            animation['channels'].append({
                'target': channel['target'],
                'sampler': channel['sampler']
            })
        
        for sampler in anim_data.get('samplers', []):
            input_acc = self.json_data['accessors'][sampler['input']]
            output_acc = self.json_data['accessors'][sampler['output']]
            
            input_data = self.get_accessor_data(input_acc)
            output_data = self.get_accessor_data(output_acc)
            
            animation['samplers'].append({
                'input': input_data,
                'output': output_data,
                'interpolation': sampler.get('interpolation', 'LINEAR')
            })
        
        self.animations.append(animation)

    def get_accessor_data(self, accessor):
        buffer_view = self.json_data['bufferViews'][accessor['bufferView']]
        buffer = self.buffers[buffer_view['buffer']]
        
        start = buffer_view.get('byteOffset', 0) + accessor.get('byteOffset', 0)
        end = start + buffer_view['byteLength']
        
        component_type = accessor['componentType']
        dtype = self.get_component_type(component_type)
        count = accessor['count']
        
        if accessor['type'] == 'SCALAR':
            shape = (count,)
        elif accessor['type'] == 'VEC2':
            shape = (count, 2)
        elif accessor['type'] == 'VEC3':
            shape = (count, 3)
        elif accessor['type'] == 'VEC4':
            shape = (count, 4)
        else:
            shape = (count,)
        
        data = np.frombuffer(buffer[start:end], dtype=dtype).reshape(shape)
        return data

    def get_component_type(self, component_type):
        type_map = {
            5120: np.int8,
            5121: np.uint8,
            5122: np.int16,
            5123: np.uint16,
            5125: np.uint32,
            5126: np.float32
        }
        return type_map.get(component_type, np.float32)

    def play_animation(self, name):
        for anim in self.animations:
            if anim['name'] == name:
                self.current_animation = anim
                self.animation_start_time = time.time()
                break

    def update_animation(self):
        if not self.current_animation:
            return
            
        current_time = time.time() - self.animation_start_time
        
        for channel in self.current_animation['channels']:
            sampler = self.current_animation['samplers'][channel['sampler']]
            node_idx = channel['target']['node']
            path = channel['target']['path']
            
            # Encontrar keyframes relevantes
            times = sampler['input']
            values = sampler['output']
            
            if current_time > times[-1]:
                current_time %= times[-1]
                
            keyframe = 0
            while keyframe < len(times) - 1 and times[keyframe + 1] < current_time:
                keyframe += 1
                
            alpha = (current_time - times[keyframe]) / (times[keyframe + 1] - times[keyframe])
            alpha = max(0, min(1, alpha))
            
            # Interpolar valores
            if path == 'translation':
                start = values[keyframe]
                end = values[keyframe + 1]
                self.nodes[node_idx]['translation'] = start + (end - start) * alpha
            elif path == 'rotation':
                # Interpolação de quatérnios (simplificada)
                self.nodes[node_idx]['rotation'] = values[keyframe]
            elif path == 'scale':
                start = values[keyframe]
                end = values[keyframe + 1]
                self.nodes[node_idx]['scale'] = start + (end - start) * alpha

    def draw_model(self):
        for i, node in enumerate(self.nodes):
            if node.get('is_root', False):  # Usando get com valor padrão
                self.draw_node(i)

    def draw_node(self, node_idx):
        node = self.nodes[node_idx]
        
        glPushMatrix()
        
        # Aplicar transformações
        glMultMatrixf(node['matrix'])
        glTranslatef(*node['translation'])
        
        # Rotação (simplificada - deveria usar quatérnios)
        if 'rotation' in node:
            angle = np.linalg.norm(node['rotation'][:3])
            if angle > 0:
                axis = node['rotation'][:3] / angle
                glRotatef(np.degrees(angle), *axis)
        
        glScalef(*node['scale'])
        
        # Desenhar malha se existir
        if node['mesh'] is not None:
            self.draw_mesh(node['mesh'])
        
        # Desenhar filhos
        for child_idx in node['children']:
            if child_idx < len(self.nodes):  # Verificação de segurança
                self.draw_node(child_idx)
        
        glPopMatrix()

    from OpenGL.GLUT import glutInit
glutInit()

def draw_mesh(self, mesh_id):
    # Aqui começa a lógica para desenhar uma malha real
    mesh = self.meshes[mesh_id]

    if 'vao' in mesh:
        # Exemplo com VAO (Vertex Array Object)
        glBindVertexArray(mesh['vao'])
        glDrawElements(GL_TRIANGLES, mesh['num_indices'], GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
    else:
        # Enquanto não implementas desenho real, usa um print informativo
        print(f"Desenhar mesh com ID: {mesh_id}")
        # glutSolidCube(0.5)  # Comentado para evitar crash

def init_gl(width, height):
    pygame.init()
    glutInit()  # <- Adiciona isto ANTES de qualquer função GLUT
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    
    gluPerspective(45, (width / height), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -5)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))


def main():
    glutInit()  # <-- Linha que faltava
    init_gl(800, 600)
    clock = pygame.time.Clock()
    
    loader = GLTFLoader()
    try:
        loader.load_gltf("animated_model.glb")  # Substitua pelo seu arquivo
    except Exception as e:
        print(f"Erro ao carregar modelo: {str(e)}")
        pygame.quit()
        return
    
    if loader.animations:
        loader.play_animation(loader.animations[0]['name'])  # Toca a primeira animação
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Atualizar animação
        loader.update_animation()
        
        # Desenhar modelo
        loader.draw_model()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
