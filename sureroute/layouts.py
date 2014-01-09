from pyramid.renderers import get_renderer
from pyramid.decorator import reify


class Layouts(object):
    @reify
    def global_template(self):
        renderer = get_renderer("templates/global_layout.jinja2")
        return renderer.implementation().macros['layout']