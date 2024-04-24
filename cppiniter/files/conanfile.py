from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import update_conandata, copy
import os


class {{{project_name_camelcase}}}Conan(ConanFile):
    name = "{{{project_name}}}"
    user = ""
{{#is_exe}}
    package_type = "application"
{{/is_exe}}
{{^is_exe}}
    package_type = "library"
{{/is_exe}}
    author = "{{{author}}} {{{email}}}"
    url = ""
    description = ""
    settings = "os", "compiler", "build_type", "arch"
{{#is_exe}}
    options = {}
{{/is_exe}}
{{^is_exe}}
    options = {"shared": [True, False], "test": [True, False], "example": [True, False]}
    default_options = {"shared": True, "test": False, "example": False}
{{/is_exe}}

    @property
    def version_name(self):
        type_dict = {"stable": "R", "snapshot": "D", "testing": "T"}
        type = type_dict.get(self.channel, "S")
        hash = os.getenv("GIT_COMMIT", "")[:6]
        return "%s.%s-%s" % (type, self.version, hash)

    def export(self):
        git = Git(self, self.recipe_folder)
        scm_url, scm_commit = git.get_url_and_commit()
        update_conandata(self, {"sources": {"commit": scm_commit, "url": scm_url}})

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=".")
        git.checkout(commit=sources["commit"])

    def requirements(self):
        self.requires("fmt/10.2.1")
{{^is_exe}}
        if self.options.test:
            self.test_requires("doctest/2.4.11")
{{/is_exe}}


    def configure(self):
        pass

    def layout(self):
        cmake_layout(self)
{{^is_exe}}
        self.cpp.source.includedirs = ["%s/install/include" % self.folders.build]
        self.cpp.build.libdirs = ["install/lib"]
        self.cpp.build.bindirs = ["install/bin"]
{{/is_exe}}

    def generate(self):
        if self.settings.os == "Windows":
            tc = CMakeToolchain(self, generator="Ninja")
        else:
            tc = CMakeToolchain(self)

        if self.version:
            tc.variables["VERSION_NAME"] = self.version_name
{{^is_exe}}
        tc.variables["BUILD_TEST"] = self.options.test
        tc.variables["BUILD_EXAMPLE"] = self.options.example
{{/is_exe}}
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

{{#is_exe}}
        if self.settings.os == "Windows":
            for dep in self.dependencies.values():
                for bindir in dep.cpp_info.bindirs:
                    copy(self, "*.dll", bindir, self.build_folder)

        if self.settings.os == "Macos":
            for dep in self.dependencies.values():
                for libdir in dep.cpp_info.libdirs:
                    copy(self, "*.dylib", libdir, self.build_folder)

        if self.settings.os == "Linux":
            for dep in self.dependencies.values():
                for libdir in dep.cpp_info.libdirs:
                    copy(self, "*.so*", libdir, self.build_folder)
{{/is_exe}}
{{^is_exe}}
        if self.options.test or self.options.example:
            if self.settings.os == "Windows":
                for dep in self.dependencies.values():
                    for bindir in dep.cpp_info.bindirs:
                        copy(self, "*.dll", bindir, self.build_folder)

            if self.settings.os == "Macos":
                for dep in self.dependencies.values():
                    for libdir in dep.cpp_info.libdirs:
                        copy(self, "*.dylib", libdir, self.build_folder)

            if self.settings.os == "Linux":
                for dep in self.dependencies.values():
                    for libdir in dep.cpp_info.libdirs:
                        copy(self, "*.so*", libdir, self.build_folder)
{{/is_exe}}


    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

{{^is_exe}}
    def package_info(self):
        self.cpp_info.libs = ["{{{project_name}}}"]

        if self.options.shared:
            self.cpp_info.defines = ["{{{project_name_uppercase}}}_DLL"]
{{/is_exe}}
