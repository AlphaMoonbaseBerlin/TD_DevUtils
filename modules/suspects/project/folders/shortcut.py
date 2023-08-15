'''Info Header Start
Name : shortcut
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 2
Savetimestamp : 2023-08-15T13:22:28.104608
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
from os import path

class path_shortcut:
    def __init__(self, directory) -> None:
        self.directory = directory
        

    def __str__(self) -> str:
        return self.directory

    def __repr__(self) -> str:
        return self.directory

    def __call__(self, *args: str) -> str:
        return path.join(self.directory, *args).replace("\\", "/")