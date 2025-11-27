import fnmatch
import sys

import graphviz
from findimports import ModuleGraph
from stdlib_list import stdlib_list

gobn = "inspect/imports2"


def graphpack(
    path, package_name, ignore_packages=None, ignore_modules=None, color_rules=None
):
    """Plot a graph from the imports of your package

    Args:
        package_name: str, you package name
        ignore_packages list of string : names of packages to ignore
        ignore_modules list of string : names of modules to ignore
        color_rules: dict of colors names to customize the graph:
            color_rules = {"foo": "purple", "bar": "blue"}
            will paint all names containing foo in purple and bar in blue.
            if several matches, the last teakes precendence.

    Returns:
        writes down a {package_name}.svg image.
    """

    if ignore_modules is None:
        ignore_modules = []
    if ignore_packages is None:
        ignore_modules = []

    modgraph = ModuleGraph()
    modgraph.external_dependencies = True
    modgraph.parsePathname(path + "/" + package_name + ".py")
    # modgraph.printImports()

    _del_modules(modgraph, ignore_modules)
    _del_inits(modgraph)
    internal_modules = set(module.label for module in modgraph.listModules())
    _del_external_packages(modgraph, internal_modules, ignore_packages)
    _create_graph(modgraph, internal_modules, gobn + ".gv", color_rules)


def _del_modules(modgraph, ignore_modules):
    """Remove the ingnoreme module list"""

    to_delete = []
    for module_name in ignore_modules:
        for act_module in modgraph.modules:
            if fnmatch.fnmatch(act_module, module_name):
                to_delete.append(act_module)

    for del_mod in to_delete:
        print(f"skipping module: {del_mod}")
        del modgraph.modules[del_mod]


def _del_inits(modgraph):
    """Remove the __inits__"""

    for module in modgraph.listModules():
        # Simplify labes of a module  if __init__ in inside
        if module.label.split(".")[-1] == "__init__":
            module.label = ".".join(module.label.split(".")[:-1])

        # enleve les imports de ce module termines par INIT et les remplace par le nom au dessus
        for import_ in module.imports.copy():
            if import_.split(".")[-1] == "__init__":
                module.imports.remove(import_)
                module.imports.add(".".join(import_.split(".")[:-1]))


def _del_external_packages(modgraph, internal_modules, ignore_packages):
    """Remove stdlib packages and user defined ignore-packages list"""

    stdlib = set(stdlib_list("3.9"))
    for module in modgraph.listModules():
        for import_ in module.imports.copy():
            # do not accept standard library
            if import_ in stdlib:
                module.imports.remove(import_)
            # simplify external dependencies
            elif import_ not in internal_modules:
                module.imports.remove(import_)
                import_ = import_.split(".")[0]

                if import_ not in ignore_packages:
                    module.imports.add(import_)


def _create_graph(modgraph, internal_modules, filename, color_rules):
    """Create the graph with  graphiz"""
    node_names = set()
    for module in modgraph.listModules():
        node_names.add(module.label)
        node_names |= module.imports

    if color_rules is None:
        color_rules = {}

    dot = graphviz.Digraph(filename, engine="dot")
    # create nodes
    for name in node_names:
        style = "" if name in internal_modules else "dashed"
        color = "black"
        for key in color_rules:
            if key in name:
                style = "filled"
                color = color_rules[key]
        dot.node(name, style=style, color=color, shape="record")
    # add edges
    for module in modgraph.listModules():
        for import_ in module.imports:
            dot.edge(module.label, import_)

    dot.render(filename, format="svg")


graphpack(
    path="/sdcard/projects/pybackup",
    package_name="pybackup",
    ignore_packages=[],
    ignore_modules=[],
    color_rules={
        "avbtp": "purple",
        "tavbp": "blue",
        "avtp": "red",
        "combu": "orange",
        "tools": "green",
        "postproc": "green",
        "mesh2curve": "green",
    },
)
