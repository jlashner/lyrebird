#ifndef SHADER_HPP
#define SHADER_HPP
#include <string> 

GLuint LoadShaders(const char * vertex_file_path,const char * fragment_file_path);
GLuint LoadShadersDef(std::string VertexShaderCode,std::string FragmentShaderCode);

#endif
