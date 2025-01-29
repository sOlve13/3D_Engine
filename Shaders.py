def load_shader_source(file_path):
    """
    Reads and returns the content of a shader file.
    
    Args:
        file_path (str): Path to the shader file
        
    Returns:
        str: Content of the shader file
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


vertex_shader_source = load_shader_source("shaders/vertexShader.glsl")

fragment_shader_source = load_shader_source("shaders/fragmentShader.glsl")

fragment_shader_lamp = load_shader_source("shaders/lampFragmentShader.glsl")

lamp_vertex_shader = load_shader_source("shaders/lampVertexShader.glsl")

lamp_fragment_shader = load_shader_source("shaders/lampFragmentShader.glsl")

texture_vertex_shader = load_shader_source("shaders/textureVertexShader.glsl")

texture_fragment_shader = load_shader_source("shaders/textureFragmentShader.glsl")
