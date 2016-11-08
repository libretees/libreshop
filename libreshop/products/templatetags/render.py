from django.template import defaultfilters, Library, Node, Template, TemplateSyntaxError, Variable

register = Library()

class RenderNode(Node):

    def __init__(self, field):
        self.obj = Variable(field.split('.')[0])
        self.template = field.split('.')[1]

    def render(self, context):
        obj = self.obj.resolve(context)
        template = Template(getattr(obj, self.template))
        rendered_field = template.render(context)
        return defaultfilters.linebreaks(rendered_field)


@register.tag
def render(parser, token):
    try:
        tag_name, field = token.split_contents()
    except ValueError as e:
        raise TemplateSyntaxError(
            '%r tag requires a single argument.' % tag_name)

    return RenderNode(field)
