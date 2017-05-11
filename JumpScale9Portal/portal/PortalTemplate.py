import jinja2


class PortalTemplate(object):

    def __init__(self, base):
        loader = jinja2.FileSystemLoader(base)
        self._env = jinja2.Environment(loader=loader)

    def render(self, _template, **kwargs):
        template = self._env.get_template(_template)

        return template.render(**kwargs)
