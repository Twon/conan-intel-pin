from conans import ConanFile, CMake, tools


class IntelPinConan(ConanFile):
    name = "intel-pin"
    version = "3.13"
    license = "MIT"
    export = ["LICENSE"]
    author = "Antony Peacock ant.peacock@gmail.com"
    url = "https://github.com/Twon/conan-intel-pin"
    description = "Pin is a dynamic binary instrumentation framework for the IA-32 and x86-64 instruction-set architectures that enables the creation of dynamic program analysis tools."
    topics = ("C++", "Tools", "Instrumentation")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

#    def source(self):
#        self.run("git clone https://github.com/memsharded/hello.git")
#        self.run("cd hello && git checkout static_shared")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
#        tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)",
#                              '''PROJECT(MyHello)
#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()''')

    def build(self):
        os_to_pin_os = { "Windows" : "msvc-windows.zip", "Linux" : "gcc-linux.tar.gz", "Macos" : "clang-mac.tar.gz" }
        version_to_file_version = { "3.13" : "3.13-98189-g60a6ef199" }
        url = ("https://software.intel.com/sites/landingpage/pintool/downloads/pin-{}-{}".format(
            version_to_file_version[self.version],
            os_to_pin_os[str(self.settings.os)]
        ))
        tools.get(url)

#        cmake = CMake(self)
#        cmake.configure(source_folder="hello")
#        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

