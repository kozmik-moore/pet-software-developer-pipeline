from pathlib import Path

def get_path_obj(*nodes: Path|str):
    return Path(*nodes)

# Directory paths
root_dir = Path('..')
data_dir = get_path_obj(root_dir, 'data')
assets_dir = get_path_obj(root_dir, 'assets')
code_dir = get_path_obj(root_dir, 'code')
products_dir = get_path_obj(root_dir, 'products')
images_dir = get_path_obj(products_dir, 'images')

# File paths
raw_data_path = get_path_obj(data_dir, 'raw_data.csv')
processed_data_path = get_path_obj(data_dir, 'processed_data.csv')

# Other variables