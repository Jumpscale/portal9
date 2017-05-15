import os


def main(j, args, params, tags, tasklet):
    page = args.page
    page.addCSS(cssContent='''
.hrdFile{
	margin: 10px 0 15px 0;
}
''')
    hrd = j.data.hrd.get(content=args.cmdstr)
    hrdFile = {}
    hrdFile['filePath'] = hrd.getStr('file.path', '')
    hrdFile['header'] = hrd.getStr('header', '')

    space = j.portal.tools.server.active.spacesloader.spaces[args.doc.getSpaceName()]
    hrdFile['hrdContent'] = open(space.model.path + hrdFile['filePath'] + ".hrd", 'r').read().replace('\n', '<br/>')

    page.addMessage('''
		<div class="hrdFile-container">
			<div class="container">
				<div class="span12">
					<h3>{header}</h3>
					<p>{hrdContent}</p>
				</div>
			</div>
		</div>
	 '''.format(**hrdFile))

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
