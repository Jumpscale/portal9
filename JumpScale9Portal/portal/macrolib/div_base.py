import re


def tag_params_to_html_attrs(tag_params):
    tag_params = [[i.strip() for i in pair.split('=')] for pair in tag_params.split('|')]
    tag_params = [('{0}="{1}"'.format(l[0], l[1]) if len(l) == 2 else l[0]) for l in tag_params]
    return ' '.join(tag_params)


def macro(q, args, params, self_closing=False, tag=None, additional_tag_params=None):
    '''
    A generic HTML tag macro, similar to div/span macros in Confluence.
    In practice, this supports any macro in this format:

        {{tag_name: id=id1|class=x y x|style=background-color: green|src=123}}

    and all attributes will be converted to HTML attributes. To close the macro, use the same macro name without any
    parameters, like:

        {{tag_name}}

    Nesting macros is through a number added to the macro name which represents the level, e.g. {{div2}}.

    Example:

        {{div}}
            {{div2 id=left-panel|class=clearbox column8}}
                {{span id=span1}}Text inside{{span}}
            {{div2}}
        {{div}}

    The generated HTML will be:

        <div>
            <div id="left-panel" class="clearbox column8">
                <span id="span1">Text inside</span>
            </div>
        </div>

    It also allows specifying the tag name explicitly, or adding additional HTML attributes. This is used to implement
    the input macros, e.g.

        {{email}}

    will generate
        <input type="email" />

    '''
    params.result = page = args.page

    match = re.match(r'{{\s*([a-zA-Z]+)(\d*):?(\s*.*?)?}}', args.macrostr, re.DOTALL)

    if not match:
        page.addMessage('Invalid syntax for macro div/span ({0})'.format(args.macrostr))
        return params

    tag_name, tag_level, tag_params = match.group(1), match.group(2), match.group(3)
    if not tag_level:
        tag_level = '1'

    if tag:
        tag_name = tag

    if tag_params:
        tag_params = tag_params_to_html_attrs(tag_params)
        if additional_tag_params:
            tag_params = tag_params + ' ' + ' '.join('{0}="{1}"'.format(k, v)
                                                     for k, v in list(additional_tag_params.items()))

    tag_stack_entry = tag_name + tag_level

    if not getattr(page, 'tags_stack', None):
        page.tags_stack = []

    # There are 3 possible situation of calling this macro
    # 1. Macro is called with parameters                                => start tag & convert macro parameters to tag
    #                                                                      attributes
    # 2. Macro is called with no parameters, but it's the first call    => start tag
    # 3. Macro is called with no parameters, but the 2nd time           => end tag
    #
    # To differentiate between 2nd & 3rd case, I add a stack to the page itself.
    #
    # Why dynamic? Because the stack is specific to this macro. But in case we want to add this functionality to other
    # macros then we must move it to PageHTML itself.
    if tag_params:
        page.addMessage('<{0} {1}>'.format(tag_name, tag_params))
        page.tags_stack.append(tag_stack_entry)
    elif page.tags_stack and page.tags_stack[-1] == tag_stack_entry:
        page.addMessage('</{0}>'.format(tag_name))
        page.tags_stack.pop()
    else:
        page.addMessage('<{0}>'.format(tag_name))
        page.tags_stack.append(tag_stack_entry)

    if self_closing:
        page.addMessage('</{0}>'.format(tag_name))
        page.tags_stack.pop()

    return params
