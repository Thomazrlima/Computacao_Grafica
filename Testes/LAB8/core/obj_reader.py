from typing import List

def my_obj_reader(filename: str) -> List:
    """Get the vertices from the file"""
    position_list = []
    vertices = []

    with open(filename, 'r') as in_file:
        for line in in_file:
            if line.startswith('v '):  # apenas vértices, não vt ou vn
                point = [float(value) for value in line.strip().split()[1:]]
                vertices.append(point)
            elif line.startswith('f '):
                face_description = [int(value.split('/')[0]) - 1 for value in line.strip().split()[1:]]
                for elem in face_description:
                    position_list.append(vertices[elem])

    return position_list
