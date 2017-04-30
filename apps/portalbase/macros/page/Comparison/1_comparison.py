from itertools import count


def main(j, args, params, tags, tasklet):
    page = args.page
    page.addCSS(cssContent='''
.comparison-block{
	border: 1px solid #CCE4E2;
	margin-bottom: 10px;
}
.comparison-block:hover{
	border: 1px solid #B0D7D5;
}
.comparison-block:hover .title{
	background-color: #62a29e;
	color: #fff;
}
.comparison-block:hover .title *{
	color: #fff;
}
.comparison-footer{
	padding: 10px 0;
	border-top: 1px solid #CCE4E2;
	margin-top: 10px;
}
.comparison-footer button{
	margin-top: 8px;
}
.text-center{
	text-align: center;
}
.comparison-block .title{
	background: #C7E1E0;
	padding: 15px;
}
.comparison-block .title small, .price small, .comparison-footer small{
	color: #8D8A8A;
}
.comparison-block .title p{
	margin-bottom: 5px;
	color: #4F918D;
	font-weight: bold;
}
.comparison-block .title p.small{
	font-size: 95%;
}
.comparison-block .title p.medium{
	font-size: 18px;
}
.comparison-block .title p.large{
	font-size: 180%;
}
.comparison-block .price{
	padding-top: 15px;
	background-color: #F1F0F0;
	border-top: 1px solid #CCE4E2;
	border-bottom: 1px solid #CCE4E2;
	margin-bottom: 10px;
	padding-bottom: 10px;
}
.comparison-block .price p{
	font-size: 30px;
	color: #767677;
	margin-bottom: 0;
}
.comparison-block .property{
	padding: 3px;
	font-size: 90%;
	padding-left: 8px;
	cursor: default;
}
.comparison-block .property:hover{
	background-color: #62a29e;
	color: #fff;
}
.comparison-block .currency{
	font-size: 60%;
}''')
    hrd = j.data.hrd.get(content=args.cmdstr)

    currency = hrd.getStr('currency', '')

    blocks = []
    for i in count(1):
        block = {}
        block['Title'] = hrd.getStr('block.{}.title.text'.format(i), '').replace(r'\n', '<br />')
        if not block['Title']:
            break
        block['TitleSize'] = hrd.getStr('block.{}.title.size'.format(i), '')
        block['SubtitleText'] = hrd.getStr('block.{}.subtitle.text'.format(i), '').replace(r'\n', '<br />')
        block['SubtitleSize'] = hrd.getStr('block.{}.subtitle.size'.format(i), '')
        block['Price'] = hrd.getStr('block.{}.price'.format(i), '')
        block['PriceSubtitle'] = hrd.getStr('block.{}.price.subtitle'.format(i), '').replace(r'\n', '<br />')
        block['Property1'] = hrd.getStr('block.{}.property.1'.format(i), '').replace(r'\n', '<br />')
        block['Property2'] = hrd.getStr('block.{}.property.2'.format(i), '').replace(r'\n', '<br />')
        block['Property3'] = hrd.getStr('block.{}.property.3'.format(i), '').replace(r'\n', '<br />')
        block['Property4'] = hrd.getStr('block.{}.property.4'.format(i), '').replace(r'\n', '<br />')
        block['OrderButtonText'] = hrd.getStr('block.{}.order.button.text'.format(i), '').replace(r'\n', '<br />')
        block['OrderButtonStyle'] = hrd.getStr('block.{}.order.button.style'.format(i), '').lower()
        block['OrderButtonSubtext'] = hrd.getStr('block.{}.order.button.subtext'.format(i), '').replace(r'\n', '<br />')
        block['OrderButtonSubLink'] = hrd.getStr('block.{}.order.button.link'.format(i), '')
        blocks.append(block)

    page.addMessage('''
		<div class="container">
		''')

    for block in blocks:
        block['i'] = 12 / len(blocks)
        page.addMessage('''
				<div class="span{i} comparison-block">
					<div class="title text-center">
						<p class="{TitleSize}">{Title}</p>
						<small>{SubtitleText}</small>
					</div>
					<div class="price text-center">
						<p><small class="currency">{currency}</small>{Price}</p>
						<small>{PriceSubtitle}</small>
					</div>
					<div class="property-container">
		'''.format(currency=currency, **block))

        if(block['Property1']):
            page.addMessage('''
				<div class="property">
					{Property1}
				</div>
			'''.format(**block))

        if(block['Property2']):
            page.addMessage('''
				<div class="property">
					{Property2}
				</div>
			'''.format(**block))

        if(block['Property3']):
            page.addMessage('''
				<div class="property">
					{Property3}
				</div>
			'''.format(**block))

        if(block['Property4']):
            page.addMessage('''
				<div class="property">
					{Property4}
				</div>
			'''.format(**block))

        page.addMessage('''
					</div>
					<div class="comparison-footer text-center">
						<small>{OrderButtonSubtext}</small>
						<br/>
						<a href="{OrderButtonSubLink}" class="btn btn-{OrderButtonStyle}">{OrderButtonText}</a>
					</div>
				</div>
		'''.format(**block))

    page.addMessage('''</div>''')
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
