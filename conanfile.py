from conans import CMake, ConanFile, tools
import os


class BrpcConan(ConanFile):
    name = "brpc"
    version = '1.3.0'
    license = "https://github.com/apache/incubator-brpc/blob/1.3.0/LICENSE"
    url = "https://github.com/jjkoshy/conan-recipes/conan-brpc"
    description = "An industrial-grade RPC framework used throughout Baidu"
    settings = "os", "os_build", "compiler", "build_type", "arch", "arch_build"
    options = {
            "shared": [True, False],
            # see the leveldb recipe in conan-leveldb/conanfile.py for why we
            # need this
            "with_snappy": [True, False] }
    default_options = {
            "shared": False,
            "with_snappy": False }
    # cmake_paths generates a file which we set as the cmake toolchain file
    generators = ('cmake_paths', 'CMakeDeps')
    exports_sources = ["CMakeLists.txt", "patches/*"]

    requires = (
        'gflags/2.2.2',
        'protobuf/3.21.4',
        'leveldb/1.23',
        'openssl/1.1.1s',)

    def config(self):
        # must build protobuf with zlib since brpc build does not make it optional
        self.options['protobuf'].with_zlib = True
        self.options['leveldb'].with_snappy = self.options.with_snappy

    @property
    def zip_folder_name(self):
        return "incubator-%s-%s" % (self.name, self.version)

    def source(self):
        zip_name = "%s.zip" % self.version
        tools.download("https://github.com/apache/incubator-brpc/archive/%s.zip" % self.version, zip_name)
        tools.unzip(zip_name)
        # TODO: move to conandata.yml
        tools.check_md5(zip_name, "0b2e4af0a9b61705d73a7a1957d9cd4f")
        os.unlink(zip_name)
        with tools.chdir(self.zip_folder_name):
            # TODO: switch to conandata.yml approach
            tools.patch(patch_file="../patches/brpc-1.3.0.patch", strip=1)

            # # add snappy to list of libs to link with if with_snappy is true
            # if self.options.with_snappy:
            #     tools.patch(patch_file="../patches/snappy.patch", strip=1)

    def configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions['CMAKE_TOOLCHAIN_FILE'] = 'conan_paths.cmake'
        # TODO: the source_subfolder should be something generic like
        # src or source-subfolder, and we should rename. change
        # cmakelists.txt also
        cmake.configure(
            defs={
                'CMAKE_POSITION_INDEPENDENT_CODE': True,
                'protobuf_MODULE_COMPATIBLE': True,
                'BUILD_BRPC_TOOLS': False,
            })
        return cmake
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", "incubator-brpc-0.9.6", keep_path=False)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["brpc"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

