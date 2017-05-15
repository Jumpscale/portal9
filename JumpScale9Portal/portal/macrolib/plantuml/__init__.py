import os
import subprocess
import hashlib
from js9 import j


class JarNotFoundException(Exception):
    pass


class GraphVizNotInstalled(Exception):
    pass


def run_plant_uml(space_name, uml, output_path):
    '''Given Plant UML text, return a path of the image inside the output path'''
    dirname = os.path.dirname(__file__)
    jar_path = os.path.join(dirname, 'plantuml.jar')

    if not os.path.exists(jar_path):
        raise JarNotFoundException('PlantUML JAR should be in "{}", but it\'s not found'.format(jar_path))

    process = subprocess.Popen(['java', '-jar', jar_path, '-pipe'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE
                               )
    img_data, err_data = process.communicate(uml)

    if err_data:
        raise GraphVizNotInstalled(err_data)

    img_name = 'img-{}.png'.format(hashlib.md5(uml).hexdigest())

    space_path = j.portal.tools.server.active.getSpace(space_name).model.path
    output_path = os.path.join(space_path, output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    open(os.path.join(output_path, img_name), 'wb').write(img_data)

    return img_name
