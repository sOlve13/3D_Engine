import glm

class Camera:
    def __init__(self, position, target, up_vector):
        self.position = glm.vec3(position)  
        self.target = glm.vec3(target) 
        self.up = glm.vec3(up_vector) 
        
        self.view_matrix = glm.mat4(1.0) 
        self.projection_matrix = glm.mat4(1.0)
        
        self.update_view_matrix()

    def update_view_matrix(self):
        self.view_matrix = glm.lookAt(self.position, self.target, self.up)

    def set_projection(self, fov, aspect_ratio, near, far):
        self.projection_matrix = glm.perspective(glm.radians(fov), aspect_ratio, near, far)

    def move(self, delta_position):
        self.position += glm.vec3(delta_position)
        self.target += glm.vec3(delta_position) 
        self.update_view_matrix()
