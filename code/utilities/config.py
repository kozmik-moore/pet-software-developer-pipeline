from pathlib import Path

def get_path_obj(*nodes: Path|str):
    return Path(*nodes)

class Directories:
    """A class for easily accessing and managing directory information
    """
    def __init__(self, name) -> None:
        self._name = name
        self._root = Path('..')
        self._location = self._root

    @property
    def name(self):
        return self._name

    @property
    def root(self):
        """Returns a path representation of the project root

        Returns:
            pathlib.Path: a Path object pointing to the root of the project directory
        """
        return self._root
    
    @property
    def path(self):
        """Returns a path representation of the object root

        Returns:
            pathlib.Path: a Path object pointing to the root of the object
        """
        return self._location
    
    def __str__(self) -> str:
        return str(self._location)

    def add_path(self, name: str,  *nodes: str|Path):
        """Add an attribute representing a path

        Args:
            name (str): The attribute name

        Raises:
            ValueError: Thrown if the attribute name already exists in the instance
        """
        if name in dir(self):
            raise ValueError(f'Directories object already has an attribute "{name}"')
        setattr(self, name, get_path_obj(*nodes))

class Data(Directories):
    def __init__(self, name: str = 'data') -> None:
        super().__init__(name)
        self._location = self._root / 'data'
        self.activities = self._location / 'pet_activities.csv'
        self.health = self._location / 'pet_health.csv'
        self.users = self._location / 'users.csv'

class Assets(Directories):
    def __init__(self, name: str = 'assets') -> None:
        super().__init__(name)
        self._location = self._root / 'assets'

class Code(Directories):
    def __init__(self, name: str = 'code') -> None:
        super().__init__(name)
        self._location = self._root / 'code'

class Products(Directories):
    def __init__(self, name: str = 'products') -> None:
        super().__init__(name)
        self._location = self._root / 'products'
        self.images = self._location / 'images'

data = Data()
assets = Assets()
code = Code()
products = Products()