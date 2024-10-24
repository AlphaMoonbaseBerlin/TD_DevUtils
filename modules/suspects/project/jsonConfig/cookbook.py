'''Info Header Start
Name : cookbook
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.11880
Info Header End'''

from .config_module import *



resolution = CollectionDict({
    "Width" : ConfigValue(
        1920, 
        validator = lambda value: value > 1, 
        comment = "Width of the element as an Integer."),
    "Height" : ConfigValue(
        1080, 
        validator = lambda value: value > 1, 
        comment = "Height of the element as an Integer.")
    }, comment = "A 2D Resolution defined with integers.")

position = CollectionDict({
    "X" : ConfigValue(
        1.0, 
        parser = lambda value: float(value), 
        comment = "x Position."),
    "Y" : ConfigValue(
        1.0, 
        parser = lambda value: float(value), 
        comment = "x Position."),
})

def fromParameter(parameter:Par):
    if parameter.style.lower() in ["float", "in",
                           "rgb", "rgba", 
                           "xy" "xyz", "xyzw",
                           "uv", "uvw", "wh"]:
        return ConfigValue(
            parameter.default,
            validator = lambda value: parameter.min <= value <= parameter.max,
            comment = parameter.help
        )
    if parameter.style.lower() in ["menu", "strmenu"]:
        return EnumValue(
            parameter.default,
            allowedValues=[
                value for value in parameter.menuNames
            ]
        )
    return ConfigValue(
        str( parameter.default )
    )
    return

def fromSequence( parsequence:Sequence):
    # Should we work us off of the existing items? Yeaah, think so.
    return CollectionDict({
        str(index) : fromParGroup( block.parGroup ) for block in enumerate( parsequence.blocks )
    })

def fromParGroup( pargroup:ParGroup):
    if pargroup.isSequence: return fromSequence( pargroup )
    if pargroup.sequence: return
    if len(pargroup) > 1: return CollectionDict({
        parameter.name : fromParameter( parameter ) 
        for parameter in pargroup
    })
    return fromParameter( pargroup[0] )

def fromCOMP( operator:COMP):
    return CollectionDict({
        parGroup.name : fromParGroup( parGroup ) 
        for parGroup in operator.customParGroups
    })