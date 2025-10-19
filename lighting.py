from pyglm import glm


def BlinnPhong(world_pos, light, view_dir, normal, object_color):
    
    #ambient
    ambientStrength = 0.2
    ambient = ambientStrength * light.getColor()
    
    #diffuse
    light_dir = glm.normalize(light.getPosition() - world_pos)
    diff_coef = glm.max(glm.dot(normal, light_dir),0.0)
    diffuse = diff_coef * light.getColor()
    
    #specular
    specular_strength = 1.0
    reflect_dir = glm.reflect(-light_dir, normal)
    spec = glm.pow(glm.max(glm.dot(view_dir, reflect_dir), 0.0), 32)
    specular = specular_strength * spec * light.getColor()

    return (ambient + diffuse + specular) * object_color