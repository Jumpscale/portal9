from itertools import count
import os


def main(j, args, params, *other_args):
    params.result = page = args.page
    page.addCSS(cssContent='''
.parallax-container{
    position: relative;
}
.parallax-container .title{
    font-weight:500;
    font-style:normal;
}
.parallax-container .title.small{
    font-size: 25px;
}
.parallax-container .title.medium{
    font-size: 30px;
}
.parallax-container .title.large{
    font-size: 35px;
}
.parallax-container .textblock-body.small{
    font-size: 13px;
}
.parallax-container .textblock-body.medium{
    font-size: 14px;
}
.parallax-container .textblock-body.large{
    font-size: 15px;
}
.parallax-container .textblock-body{
    margin: 0 0 20px 0;
    font-weight:200;
    font-style:normal;
}
.parallax-container .story{
    margin: 0 auto;
    min-width: 980px;
    overflow: auto;
    width: 980px;
}
.parallax-container .story .float-left, .story .float-right{
    padding: 20px;
    position: relative;
    width: 350px;
    margin-top: 100px;
    background: rgba(0, 0, 0, 0.7);
}
.parallax-container .float-left{
    float: left;
}
.parallax-container .float-right{
    float: right;
}
.parallax-container .slide{
    width: 100%;
    color: #fff;
    margin: 0 auto;
    padding: 0;
    overflow: hidden;
}
''')

    page.addJS('/jslib/jquery/jquery.localscroll-1.2.7-min.js')
    page.addJS('/jslib/jquery/jquery.parallax-1.1.3.js')
    page.addJS('/jslib/jquery/jquery.scrollTo-1.4.2-min.js')

    hrd = j.data.hrd.get(content=args.cmdstr)

    space = j.portal.tools.server.active.spacesloader.spaces[args.doc.getSpaceName()]
    imagedir = j.sal.fs.joinPaths(space.model.path, '.files', 'img/')

    slides = []
    for i in count(1):
        slide = {}
        slide['Title'] = hrd.getStr('slide.{}.title.text'.format(i), '').replace(r'\n', '<br />')
        if not slide['Title']:
            break
        slide['TitleSize'] = hrd.getStr('slide.{}.title.text.size'.format(i), 'medium')
        if os.path.isfile(imagedir + hrd.getStr('slide.{}.image.path'.format(i), '')):
            # check if can find image under .files/img by the given name
            slide['ImagePath'] = '/$$space/.files/img/' + hrd.getStr('slide.{}.image.path'.format(i), '')
        else:
            # image from full url
            slide['ImagePath'] = hrd.getStr('slide.{}.image.path'.format(i), '')
        slide['ImageHeight'] = hrd.getStr('slide.{}.image.height'.format(i), '800')
        slide['TextBlockPosition'] = hrd.getStr('slide.{}.textblock.position'.format(i), '')
        slide['TextBlockBody'] = hrd.getStr('slide.{}.textblock.body'.format(i), '').replace(r'\n', '<br />')
        slide['TextBlockBodySize'] = hrd.getStr('slide.{}.textblock.body.size'.format(i), 'medium')
        slide['ScrollSpeed'] = hrd.getStr('slide.{}.scroll.speed'.format(i), '0.3')
        slides.append(slide)

    page.addMessage('''
        <div class="container">
            <div class="parallax-container">
        ''')

    for slide in slides:
        slide['index'] = slides.index(slide) + 1
        page.addMessage('''
            <div id="slide{index}" class="slide" style=" background:url({ImagePath}) 50% 0 no-repeat fixed; height: {ImageHeight}px; ">
                <div class="story">
                    <div class="float-{TextBlockPosition}">
                    <h2 class="title {TitleSize}">{Title}</h2>
                    <p class="textblock-body {TextBlockBodySize}">{TextBlockBody}</p>
                    </div>
                </div>
            </div>
            '''.format(**slide))

    page.addMessage('''
        </div>
            </div>
        ''')

    for slide in slides:
        slide['index'] = slides.index(slide) + 1
        page.addJS(jsContent=''' $('#slide{index}').parallax("50%", {ScrollSpeed}); '''.format(**slide))

    return params


def match(*whatever):
    return True
