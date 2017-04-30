
def main(j, args, params, *other_args):
    params.result = page = args.page
    page.addCSS('/jslib/famous/css/famous.css')
    page.addCSS('/jslib/famous/css/app.css')

    page.addJS('/jslib/famous/js/classList.min.js')
    page.addJS('/jslib/famous/js/functionPrototypeBind.js')
    page.addJS('/jslib/famous/js/requestAnimationFrame.js')
    page.addJS('/jslib/famous/js/require.js')
    page.addJS('/jslib/famous/js/famous.js')
    page.addJS('/jslib/famous/js/famous_init.js')

    images = [line.split(':') for line in args.cmdstr.splitlines()]

    js_beginning = '''define('app/templates', function(require, exports, module) { module.exports = {'''

    image_parts = []
    for i, (title, subtitle, img) in enumerate(images):
        image_parts.append(
            ''' '{index}': '<section><div class="full-image" style="background-image: url({img});"></div><div class="overlay-content light-bg"><h1>{title}</h1><h3>{subtitle}</h3></div></section>' '''.format(index=(i + 1), img=img, title=title, subtitle=subtitle))

    js_end = '''} });'''

    page.addJS(jsContent=js_beginning + ', '.join(image_parts) + js_end)

    page.addJS(jsContent='''require.config({
                baseUrl: '/jslib/famous/js'
            });
            require(['famous_init']);''')

    page.addMessage('<div id="famous-container"></div>')

    return params


def match(*whatever):
    return True
