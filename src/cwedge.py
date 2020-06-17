import os
from os import path

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

    def put(self, location=None, mount=False):
        if location != None:
            self.location = location
        if self.location != None:
            return
        full_loc = path.join(loc, self.name)
        os.makedirs(full_loc, exists_ok=True)
        file_obj = open(full_loc, "w+")
        file_obj.write(self.content)
        file_obj.close()
        if mount:
            self.content = None

def default():
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



# Returns a dict mapping names to representations of directories and files
def new(loc=os.curdir):
    if not path.exists(loc):
        return None
    if path.isfile(loc):
        return { path.basename(loc) : VirtualFile(path.basename(loc), location=loc) }
    children = dict()
    for entry in os.scandir(loc):
        children.apply(new_model(entry.loc))
    return { path.basename(loc) : children }


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


def update_project(model, loc=os.curdir, replace=False):
    for title in model.keys():
        loc_here = path.join(loc, title)
        if path.exists(loc_here):
            if type(model[title]) == dict:
                path.makedirs(loc_here, exists_ok=True)
                update_project(model[title], loc_here, replace)
            elif replace and type(model[title]) == VirtualFile:
                model[title].make(loc)
            else:
                #! replace this later
                raise Exception("ERROR: unsupported model element")

def mount(model, loc=os.curdir):
    pass

def setup_project(loc=os.curdir, config=None):
    update_project(default_model())












