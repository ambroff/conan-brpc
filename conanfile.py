from conans import CMake, ConanFile, tools
import os

class BrpcConan(ConanFile):
    name = "brpc"
    version = "0.9.5"
    license = "https://github.com/brpc/brpc/blob/master/LICENSE"
    url = "https://github.com/ambroff/conan-brpc"
    description = "A library that provides an embeddable, persistent key-value store for fast storage."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    source_tgz = 'https://github.com/brpc/brpc/archive/%s.tar.gz' % version
    checksum = '101f05858650a810c90e4872338222a1a3bf3b24de7b7d74466814e6a95c2d28'

    requires = ()

    def source(self):
        self.output.info("Downloading %s" %self.source_tgz)
        tools.get(self.source_tgz, sha256=self.checksum)

    @property
    def subfolder(self):
        return "brpc-%s" % self.version

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(
            source_folder='brpc-{}'.format(self.version),
            defs={
                'CMAKE_POSITION_INDEPENDENT_CODE': True,
            })
        return cmake
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", src=self.subfolder, keep_path=False)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["brpc"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
