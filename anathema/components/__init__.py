from os import listdir, path
import importlib


def load_component_definitions():
    modules = listdir(path.dirname(__file__))
    for module in modules:
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        yield module[:-3]


def initialize_class_from_module(module_name: str):
    class_name = module_name.capitalize()
    module = importlib.import_module('components.' + module_name)
    print(f"Loading Component {class_name}")
    return module.__dict__.get(class_name)


def all_components():
    for component in load_component_definitions():
        component_class = initialize_class_from_module(component)
        yield component_class
