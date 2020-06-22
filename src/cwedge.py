import json
import os
from os import makedirs
from os.path import exsits, getmtime, join, splitext
import time



def jsonize(dct):
    """ Remvoes non-json elements from a dictionary.
    Converts VirtualFile objects to the integral value 1.
    Content stored in VirtualFile is lost. Write to file to avoid loss.
    Returns a dict in json format.
    """
    result = dict()
    for k, v in dct.items():
        #! all keys should be strings
        v_t = type(v)
        if v_t == VirtualFile:
            result[k] = 1
        if v_t == dict:
            result[k] = jsonize(v)
        if v_t == list or v_t == tuple:
            result[k] = [jsonize(item) for item in v]
        elif v is None or v_t in [str, int, float, bool]:
            result[k] = v
        else:
            raise Exception("ERROR: {} to json dict is not supported".format(v_t))
    return result



class Project:
    def __init__(self, path=os.curdir):
        self.main_path = path
        self.config_path = join(path, "project.json")
        self.is_fresh = not exists(self.config_path)
        self.ran_subs = False
        self.on_setup = []
        self.build_rules = dict()
        self.autos = dict()
        self.perm = {
            "name": "Project",
            "version": "0.0.0",
            "author": "",
            "license": "",
            "structure": {},
            "targets": [],
            "tests": [],
            "dependencies": {},
            "includes": [],
            "build_scripts": [],
        }

    def json_data(self):
        return jsonize(self.perm)

    def str_data(self):
        return json.dumps(self.json_data())

    def save(self):
        cfg_file = open(self.config_path, "w+")
        json.dump(self.json_data(), cfg_file)
        self.is_fresh = False

    def __del__(self):
        self.save()

    def setup(self):
        for func in self.on_setup:
            func(self)

    def add_setup(self, func):
        """ This method decorates a function that will only run
        when the project is fresh.
        """
        self.on_setup.append(func)
        if self.is_fresh:
            func(self)
        return func

    def add_structure(self, dct, path=None):
        if path == None:
            path = self.main_path
        # Internal function
        def merge_structs(dct1, dct2, pth):
            for k, v in dct1.items():
                v_t = type(v)
                inner_pth = join(pth, k)
                if v_t == dict:
                    if k in dct2.keys():
                        v2_t = type(dct2[k])
                        if v2_t == dict:
                            # Merge items from dct1/$k into dct2/$k
                            merge_structs(dct1[k], dct2[k], inner_pth)
                        else:
                            raise Exception("ERROR: File and directory with same name")
                    else:
                        dct2[k] = v
                else:
                    if k in dct2.keys():
                        print("(!) Structure already exists here, ignoring {}.".format(inner_path))
                    else:
                        dct2[k] = v
        # / Internal Function
        merge_structs(self.perm["structure"], path)

    def make_structure(self, path=None, struct=None):
        if path == None:
            path = self.main_path
        if struct == None:
            struct = self.perm["structure"]
        for k, v in struct.items():
            v_t = type(v)
            inner_path = join(path, k)
            if v_t == dict:
                makedirs(inner_path)
                self.make_structure(inner_path, struct[k])
            else:
                if not exists(inner_path):
                    open(inner_path, "a+").close()

    def add_targets(self, *targets):
        self.perm["targets"] += targets

    def add_includes(self, *includes):
        self.perm["includes"] += includes

    def add_rule(self, target, dependencies):
        def decorator(func):
            for dep in dependencies:
                if not (dep in self.perm["dependencies"][target]):
                    self.perm["dependencies"][target].append(dep)
                self.build_rules[target] = func
            return func
        return decorator

    def add_auto(self, name, **kwargs):
        def decorator(func):
                self.autos[name] = (func, kwargs)
            return func
        return decorator

    def set_xpath(self, path):
        self.perm["xpath"] = path

    def set_opath(self, path):
        self.perm["opath"] = path

    def set_test_xpath(self, path):
        self.perm["test_xpath"] = path

    def set_test_opath(self, path):
        self.perm["test_opath"] = path

    def add_subscript(self, path):
        if not (path in self.perm["build_scripts"]):
            self.perm["build_scripts"].append(path)

    def run_subscripts(self):
        for path in self.perm["build_scripts"]:
            execfile(path)
        self.ran_subs = True

    def do_auto(self, name, **kwargs):
        #! This might be fronked up
        auto = self.autos[name]
        func = auto[0]
        prekwargs = auto[1]
        func(**prekwargs, **kwargs)

    def build(self, target):
        if not self.ran_subs:
            self.run_subscripts()
        # Build dependencies recursively
        for dep in self.perm["dependencies"][target]:
            if getmtime(target) < getmtime(dep):
                self.build(dep)
        # call registered build funcion
        self.build_rules[target]()


def default_setup(project):
    project.add_structure({
        "build": {
            "bin": {
                "tests": {
                },
                "programs": {
                }
            },
            "parts": {
                "libraries": {
                },
                "tests": {
                },
                "programs": {
                },
            }
        },
        "programs": {},
        "libraries": {},
        "docs": {},
        "tests": {},
    })
    project.set_xpath("build/bin/programs/")
    project.set_opath("build/parts/programs/")
    project.set_test_xpath("build/bin/tests/")
    project.set_test_opath("build/parts/tests/")


def default_addlib(project, name):
    project.add_strucrure({
        name : {
            "include": {
                name : {}
            },
            "src": {},
            "test": {},
        }
    }, join(project.main_path, "libraries"))


def interactive_build(project):
    print(" ----- Interactive Build Textual Interface ----- ")
    done = False
    while not done:
        resp = input("!> ").split()
        # Check if resp matches builds
        if resp[0] == "build":
            project.build(resp[1])
            continue
        # Check if resp matches automations
        for auto_name in self.autos.keys():
            if resp[0] == auto_name:
                print("Running automation {}".format(auto_name))
                project.do_auto(auto_name, resp[0:])
    print(" ----------------------------------------------- ")




