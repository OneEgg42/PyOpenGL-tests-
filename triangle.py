import numpy
import glfw
from OpenGL.GL import *

def check_for_success(shader_ID):
    status = glGetShaderiv(shader_ID, GL_COMPILE_STATUS)
    return status == GL_TRUE

if not glfw.init():
    raise Exception("glfw failed")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
glfw.window_hint(glfw.VISIBLE, GL_TRUE)
glfw.window_hint(glfw.RESIZABLE, GL_FALSE)

window = glfw.create_window(720, 480, "triangle", None, None)

if not window:
    glfw.Terminate()
    raise Exception("window failed to create!")

glfw.make_context_current(window)
glViewport(0,0,720,480)

glClearColor(0.5,0.5,0.5,1)

vertices = [
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0
    ]

vao_id = glGenVertexArrays(1)
glBindVertexArray(vao_id)
glEnableVertexAttribArray(0)

vbo_id = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
vertices = numpy.array(vertices, dtype=numpy.float32)
glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

"""
explaination of the below line:

If a named buffer object is bound,
then the 6th parameter of glVertexAttribPointer is treated as a byte offset
into the buffer object's data store.
But the type of the parameter is a pointer anyway (c_void_p).
So if the offset is 0, then the 6th parameter can either be None or c_void_p(0)
else the offset has to be caste to c_void_p(0):

"""

#                                           THIS HAS TO BE NONE
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

with open("vertexShader.txt") as vs:
    vertex_shader_source = vs.read()
with open("fragmentShader.txt") as fs:
    fragment_shader_source = fs.read()

#vertex shader
vertex_shader_ID = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vertex_shader_ID, vertex_shader_source)
glCompileShader(vertex_shader_ID)
if not check_for_success(vertex_shader_ID):
    glfw.terminate()
    raise Exception("vertex shader failed")
#fragment shader
fragment_shader_ID = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fragment_shader_ID, fragment_shader_source)
glCompileShader(fragment_shader_ID)
if not check_for_success(fragment_shader_ID):
    glfw.terminate()
    raise Exception("fragment shader failed")
#shader program
shader_program_ID = glCreateProgram()
glAttachShader(shader_program_ID, vertex_shader_ID)
glAttachShader(shader_program_ID, fragment_shader_ID)
glLinkProgram(shader_program_ID)

status = glGetProgramiv(shader_program_ID, GL_LINK_STATUS)
if status != GL_TRUE:
    glfw.terminate()
    raise Exception("shader program failed")

glUseProgram(shader_program_ID)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)

    glBindVertexArray(vao_id)
    glDrawArrays(GL_TRIANGLES, 0, len(vertices))
    
    glfw.swap_buffers(window)
    
glDetachShader(shader_program_ID, vertex_shader_ID);
glDetachShader(shader_program_ID, fragment_shader_ID);
glDeleteShader(vertex_shader_ID);
glDeleteShader(fragment_shader_ID);
glDeleteProgram(shader_program_ID);

glDeleteVertexArrays(1, [vao_id])
glDeleteBuffers(1, [vbo_id])

glfw.terminate()
