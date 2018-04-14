from conans import ConanFile, CMake, tools


class JsonfortranConan(ConanFile):
    name = "json-fortran"
    version = "6.2.0"
    license = "https://github.com/jacobwilliams/json-fortran/blob/master/LICENSE"
    url = "https://github.com/jacobwilliams/json-fortran"
    description = "A Fortran 2008 JSON API"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ["src/*"]

    def source(self):
        tools.replace_in_file("src/CMakeLists.txt", "project ( jsonfortran NONE )",
                              '''project(json-fortran NONE)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="src")
        cmake.build()
        cmake.install()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = [self.name]

