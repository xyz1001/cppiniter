from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import update_conandata
import os


class {{{project_name_camelcase}}}Conan(ConanFile):
    name = "{{{project_name}}}"
    default_user = "bytelloshare"
    package_type = "library"
    author = "{{{author}}} {{{email}}}"
    url = ""
    description = ""
    topics = ("bytelloshare")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "test": [True, False]}
    default_options = {"shared": True, "test": False}

    def _make_version(self):
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
        if self.options.test:
            self.test_requires("doctest/2.4.11")

    def configure(self):
        pass

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["VERSION_NAME"] = self._make_version()
        tc.variables["BUILD_TEST"] = self.options.test
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["{{{project_name}}}"]

        if self.options.shared:
            self.cpp_info.defines = ["{{{project_name_uppercase}}}_DLL"]
