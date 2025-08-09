from pathlib import Path
from os.path import exists

def get_path_obj(*nodes: Path|str):
    return Path(*nodes)

class Directories:
    """A class for easily accessing and managing directory information
    """
    def __init__(self, root: str|Path = Path('.'), project_root: str|Path = Path('.')) -> None:
        self._root = Path(root) if isinstance(root, str) else root
        self._project_root = Path(project_root) if isinstance(project_root, str) else project_root

    @property
    def root(self):
        """Returns the `Path` object pointing to this instance's root

        Returns:
            pathlib.Path: a Path object
        """
        return self._root

    @property
    def top(self):
        """Returns the `Path` object pointing to the project's root'

        Returns:
            pathlib.Path: a Path object
        """
        return self._project_root
    
    @property
    def exists(self):
        """Checks whether the instance root exists

        Returns:
            bool: `True` if the instance root exists
        """
        return exists(self._root)

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
    
    def __str__(self) -> str:
        return str(self._root)
    
    def __truediv__(self, other) -> Path:
        if isinstance(other, (Path)) or isinstance(other, str):
            return self._root / other
        else:
            return NotImplemented
        
class Root(Directories):
    """A `Directories` created specifically for use in this project structure. Assumes that the project root is one level up
    """
    def __init__(self, root = Path('..'), project_root = Path('..')) -> None:
        super().__init__(root, project_root)

class Data(Root):
    """A `Directories` referencing the `data` directory, found one level up
    """
    def __init__(self, root = Path('../data')) -> None:
        super().__init__(root)
        self.activities = self / 'pet_activities.csv'
        self.health = self / 'pet_health.csv'
        self.users = self / 'users.csv'

class Assets(Root):
    """A `Directories` referencing the `assets` directory, found one level up
    """
    def __init__(self, root = Path('../assets')) -> None:
        super().__init__(root)

class Code(Root):
    """A `Directories` referencing the `code` directory, found one level up
    """
    def __init__(self, root = Path('../code')) -> None:
        super().__init__(root)

class Products(Root):
    """A `Directories` referencing the `products` directory, found one level up
    """
    def __init__(self, root = Path('../products')) -> None:
        super().__init__(root)
        self._images = self / 'images'

    @property
    def images(self):
        return self._images

data = Data()
assets = Assets()
code = Code()
products = Products()