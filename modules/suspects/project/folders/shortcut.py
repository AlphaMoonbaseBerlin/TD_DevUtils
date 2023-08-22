

'''Info Header Start
Name : shortcut
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

import pathlib
class path_shortcut:
    def __init__(self, directory) -> None:
        self.directory = directory
        

    def __str__(self) -> str:
        return self.directory

    def __repr__(self) -> str:
        return self.directory

    def __call__(self, *args: str, createParent = False, createPath = False) -> pathlib.Path:
        pathObject = pathlib.Path(*args)
        if createParent: pathObject.parent.mkdir( parents = True, exist_ok=True)
        if createPath: pathObject.mkdir( parents = True, exist_ok=True)
        return pathObject