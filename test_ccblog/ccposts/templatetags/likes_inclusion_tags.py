from secretballot.models import Vote

from django import template

from likes.utils import can_vote, likes_enabled

register = template.Library()


@register.inclusion_tag('cclikes/inclusion_tags/cclikes_extender.html', takes_context=True)

def likes(context, obj, template=None):
    """
           Register a callable as an inclusion tag:

           @register.inclusion_tag('results.html')
           def show_results(poll):
               choices = poll.choice_set.all()
               return {'choices': choices}
    """
    if template is None:
        template = 'cclikes/inclusion_tags/cclikes.html'
    request = context['request']
    import_js = False
    if not hasattr(request, '_django_likes_js_imported'):
        setattr(request, '_django_likes_js_imported', 1)
        import_js = True
    try:
        model_name = obj._meta.model_name
    except AttributeError:
        model_name = obj._meta.module_name
    context.update({
        'template': template,
        'content_obj': obj,
        'likes_enabled': likes_enabled(obj, request),
        'can_vote': can_vote(obj, request.user, request),
        'content_type': "-".join((obj._meta.app_label, model_name)),
        'import_js': import_js
    })
    return context

    def inclusion_tag(self, filename, func=None, takes_context=None, name=None):
        def dec(func):
            params, varargs, varkw, defaults = getargspec(func)
            function_name = (name or getattr(func, '_decorated_function', func).__name__)
            @functools.wraps(func)
            def compile_func(parser, token):
                bits = token.split_contents()[1:]
                args, kwargs = parse_bits(
                    parser, bits, params, varargs, varkw, defaults,
                    takes_context, function_name,
                )
                return InclusionNode(
                    func, takes_context, args, kwargs, filename,
                )
            self.tag(function_name, compile_func)
            return func
        return dec
