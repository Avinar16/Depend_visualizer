import requests
from graphviz import Digraph


def get_package_info(package_name):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Не удалось получить информацию о пакете: {package_name}")


def parse_dependencies(data):
    dependencies = []
    try:
        releases = data['info']['requires_dist'] or []
        for release in releases:
            dependencies.append(release.split(' ')[0])
        return dependencies
    except KeyError:
        return dependencies


def visualize_dependencies(package_name, dependencies):
    dot = Digraph(comment='Package Dependencies')
    dot.node(package_name, package_name)
    for dep in dependencies:
        dot.node(dep, dep)
        dot.edge(package_name, dep)
    print(dot.source)
    dot.render('dependency_graph', format='pdf', cleanup=True)

def main(package_name):
    package_data = get_package_info(package_name)
    dependencies = parse_dependencies(package_data)
    print(f"Зависимости для пакета {package_name}: {dependencies}")
    visualize_dependencies(package_name, dependencies)


if __name__ == "__main__":
    main(input())

