import os


def main(j, args, params, tags, tasklet):
    page = args.page
    page.addCSS(cssContent='''
.bigpicture{
	margin: 10px 0 15px 0;
}
.bigpicture-container{
	text-align: center;
}
.subtitle{
	margin-bottom: 10px;
	display: block;
}
.subtitle-paragraph{
	margin-bottom: 5px;
}
.bigpicture-container h1.small{
	font-size: 25px;
}
.bigpicture-container h1.medium{
	font-size: 30px;
}
.bigpicture-container h1.large{
	font-size: 35px;
}
.bigpicture-container h1.xlarge{
	font-size: 40px;
}
.subtitle.small, .subtitle-paragraph.small, .subtitle-link.small{
	font-size: 14px;
}
.subtitle.medium, .subtitle-paragraph.medium, .subtitle-link.medium{
	font-size: 16px;
}
.subtitle.large, .subtitle-paragraph.large, .subtitle-link.large{
	font-size: 18px;
}
''')
    hrd = j.data.hrd.get(content=args.cmdstr)
    bigpicture = {}
    bigpicture['picturePath'] = ""
    bigpicture['titleText'] = hrd.getStr('title.text', '')
    bigpicture['titleSize'] = hrd.getStr('title.size', 'medium')
    bigpicture['subtitleText'] = hrd.getStr('subtitle.text', '')
    bigpicture['subtitleSize'] = hrd.getStr('subtitle.size', 'medium')
    bigpicture['paragraphText'] = hrd.getStr('paragraph.text', '')
    bigpicture['paragraphSize'] = hrd.getStr('paragraph.size', 'medium')
    bigpicture['subtitleLink'] = hrd.getStr('subtitle.link', '')
    bigpicture['subtitleLinkText'] = hrd.getStr('subtitle.link.text', '')
    bigpicture['subtitleLinkSize'] = hrd.getStr('subtitle.link.size', 'medium')

    # check if can find image under .files/img by the given name
    space = j.portal.tools.server.active.spacesloader.spaces[args.doc.getSpaceName()]
    imagedir = j.sal.fs.joinPaths(space.model.path, '.files', 'img/')

    if os.path.isfile(imagedir + hrd.getStr('picture.path', '')):
        bigpicture['picturePath'] = '/$$space/.files/img/' + hrd.getStr('picture.path', '')
    else:
        # image from full url
        bigpicture['picturePath'] = hrd.getStr('picture.path', '')

    page.addMessage('''
		<div class="bigpicture-container">
			<div class="container">
				<h1 class="title {titleSize}">{titleText}</h1>
				<div class="span10 offset1">
					<img class="bigpicture img-rounded" src="{picturePath}">
					<div class="subtitle-container">
						<strong class="subtitle {subtitleSize}">{subtitleText}</strong>
						<p class="subtitle-paragraph {paragraphSize}">{paragraphText}</p>
						<a class="subtitle-link {subtitleLinkSize}" href="{subtitleLink}">{subtitleLinkText}</a>
					</div>
				</div>
			</div>
		</div>
	 '''.format(**bigpicture))

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
