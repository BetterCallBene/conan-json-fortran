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

    def build_requirements(self):
        if self.settings.arch == "armv8":
            self.build_requires("CrossGccConan/5.4.0@php/stable")

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

