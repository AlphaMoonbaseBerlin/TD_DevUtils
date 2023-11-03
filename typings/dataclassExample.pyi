from dataclasses import dataclass, field

@dataclass
class testDataclass:
    requiredAttribute: int = field()
    defaultAttribute = field(default='Foobar', init=True)