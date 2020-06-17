import os
from os import path as pth

class VirtualFile:
    def __init__(self, name, content=None, location=None):
        self.name = name
        self.content = content
        self.location = location

    def reset(self, content=None, location=None):
        self.content = content
        self.location = location

    def dislocate(self):
        if self.location == None:
            return
        file_obj = open(self.location, "r")
        self.content = f.read()
        file_obj.close()
        self.location = None

    def make(self, path=None, mount=False):
        if path != None:
            self.location = path
        if self.location != None:
            return
        full_path = pth.join(path, self.name)
        os.makedirs(full_path, exists_ok=True)
        file_obj = open(full_path, "w+")
        file_obj.write(self.content)
        file_obj.close()
        if mount:
            self.content = None


def default_model():
    return {
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
                }
            },
        },
        "libraries": {
        },
        "programs": {
        }
    }


def update_project(model, path=os.curdir, replace=False):
    for title in model.keys():
        path_here = pth.join(path, title)
        if pth.exists(path_here)):
            if type(model[title]) == dict:
                pth.makedirs(path_here, exists_ok=True)
                update_project(model[title], path_here, replace)
            elif replace and type(model[title]) == VirtualFile:
                model[title].make(path)
            else:
                #! replace this later
                raise Exception("ERROR: unsupported model element")

# Returns a dict mapping names to representations of directories and files
def new_model(path=os.curdir):
    if not pth.exists(pth):
        return None
    if pth.isfile(path):
        return { pth.basename(path) : VirtualFile(pth.basename(path), location=path) }
    children = dict()
    for entry in os.scandir(path):
        children.apply(new_model(entry.path)
    return { pth.basename(path) : children }

def new_library(name):
    return { name : {
        "include": {
            name : {
            }
        },
        "src": {
        },
        "test": {
        },
    }}


def mount_model(model, path=os.curdir):
    pass


