import dataclasses


@dataclasses.dataclass
class Player:
    full_name: str
    name: str = dataclasses.field(init=False)
    tag: str = dataclasses.field(init=False)
    name_variations: set[str] = dataclasses.field(init=False)

    def __post_init__(self):
        self.name = self.full_name.split('#')[0]
        self.tag = self.full_name.split('#')[1]
        self.name_variations = self.create_name_variations()
        
    def create_name_variations(self):
        name_under = self.name.replace(' ', '_')
        name_space = self.name.replace('_', ' ')
        return {
            self.name,
            name_under,
            name_space,
            self.name + self.tag,
            name_under + self.tag,
            name_space + self.tag,
            f'{self.name} {self.tag}',
            f'{name_under} {self.tag}',
            f'{name_space} {self.tag}',
            f'{self.name}_{self.tag}',
            f'{name_under}_{self.tag}',
            f'{name_space}_{self.tag}',
            self.tag + self.name,
            self.tag + name_under,
            self.tag + name_space,
            f'{self.tag} {self.name}',
            f'{self.tag} {name_under}',
            f'{self.tag} {name_space}',
            f'{self.tag}_{self.name}',
            f'{self.tag}_{name_under}',
            f'{self.tag}_{name_space}',
        }