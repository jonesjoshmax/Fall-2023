from stl import mesh


class Vertexes:
    def __init__(self, file):
        self.filename = file

    def stl_to_vertices(self):
        mesh_data = mesh.Mesh.from_file(self.filename)
        vertices = mesh_data.vectors.reshape(-1, 3)
        return vertices
