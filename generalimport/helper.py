import re
import tomllib
from pathlib import Path


def _get_optional_dependencies_from_path(path):
    pyproject = tomllib.loads(Path(path).read_text())
    return pyproject["project"]["optional-dependencies"]

def _get_links_from_optional_dependencies(optional_dependencies, name):
    links = set()
    for group_name, dependencies in optional_dependencies.items():
        formatted_group_name = f"{name}[{group_name}]"
        for value in dependencies:
            dependency_name = re.search(r"[\w-]+", value).group()
            nested_group_names_str = re.search(r"\[(.+)]", value)

            # Value has a nested group
            if nested_group_names_str:
                nested_group_names = nested_group_names_str.groups()[0].split(",")
                # The nested group is referencing main package
                if dependency_name == name:
                    for nested_group_name in nested_group_names:
                        formatted_nested_group_name = f"{dependency_name}[{nested_group_name}]"
                        links.add((formatted_nested_group_name, formatted_group_name))
                # The nested group is referencing an external package
                else:
                    links.add((dependency_name, formatted_group_name))
            # Value is a singular package
            else:
                links.add((dependency_name, formatted_group_name))
    return links

def _process(link, result):
    product, group = link
    group = re.search(r"\[(.+)]", group).groups()[0]
    if "[" not in product:
        if product not in result:
            result[product] = []
        if group in result[product]:
            return False
        result[product].append(group)
        return True
    else:
        added = False
        for dependency, groups in result.items():
            if product in groups and group not in groups:
                groups.append(group)
                added = True
        return added



def _structure(links):
    result = {}
    while [link for link in links if _process(link=link, result=result)]:
        pass
    return {key: result[key] for key in sorted(result)}

 # if not include or key in include

def _format_pkg_name(name):
    return name.replace('.', '_').replace('-', '_')

def _render(structure, include):
    include = [_format_pkg_name(name=name) for name in include]
    structure = {_format_pkg_name(name=name): value for name, value in structure.items()}
    names_in_include_and_not_structure = sorted(list(set(include) - set(structure.keys())))

    lines = ["from generalimport import generalimport",
             "generalimport("]

    lines.extend([f'    "{name}",' for name in names_in_include_and_not_structure])

    for name, groups in structure.items():
        comment = include and name not in include
        comment = "# " if comment else ""
        if len(groups) > 1:
            groups_str = str(tuple(groups)).replace("'", '"')
        else:
            groups_str = f'"{groups[0]}"'

        lines.append(f"    {comment}{name}={groups_str},")
    lines.append(")")
    return "\n".join(lines)


def generate_import_messages(path, name, include=None):
    optional_dependencies = _get_optional_dependencies_from_path(path=path)
    links = _get_links_from_optional_dependencies(optional_dependencies=optional_dependencies, name=name)
    structure = _structure(links=links)
    return _render(structure=structure, include=include)





