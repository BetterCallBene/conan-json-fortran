from conans import ConanFile, CMake, tools
import os

class JsonfortranConan(ConanFile):
    name = "jsonfortran"
    version = "6.2.0"
    license = "https://github.com/jacobwilliams/json-fortran/blob/master/LICENSE"
    url = "https://github.com/jacobwilliams/json-fortran"
    description = "A Fortran 2008 JSON API"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ["src/*"]

    def build_requirements(self):
        if self.settings.arch == "armv8":
            self.build_requires("CrossGccConan/5.4.0@php/stable")

    def source(self):
        tools.replace_in_file("src/CMakeLists.txt", "string ( TOLOWER ${CMAKE_PROJECT_NAME}-${CMAKE_Fortran_COMPILER_ID} PACKAGE_NAME )", 
                   "string ( TOLOWER ${CMAKE_PROJECT_NAME} PACKAGE_NAME )")
        tools.replace_in_file("src/CMakeLists.txt", 'set ( PACKAGE_VERSION "${PACKAGE_NAME}-${VERSION}" )', 'set( PACKAGE_VERSION "${PACKAGE_NAME}")')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="src")
        cmake.build()
        cmake.install()
        if self.settings.arch != "armv8":
            self.output.info("Testing json_fortran")
            self.run('make check')
        #cmake.test()
        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        if self.settings.arch != "armv8":
            self.copy("*", src="bin", dst="tests")
            self.copy("*.json", src="files", dst="files")
            self.copy("*.F90", src="src/src/tests", dst="examples")

    def package_info(self):
        self.cpp_info.libdirs=[os.path.join('jsonfortran', 'lib')]
        self.env_info.jsonfortran_DIR = os.path.join(self.package_folder, 'jsonfortran', 'cmake')
