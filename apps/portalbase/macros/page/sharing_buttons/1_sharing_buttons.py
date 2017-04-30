
def main(j, args, params, *other_args):
    params.result = page = args.page

    page.addCSS('/jslib/kibana/css/font-awesome.min.css')
    page.addCSS('/jslib/sharing-buttons/css/sharing-buttons.css')

    share_info = {
        'facebook': {
            'url': '''javascript:var d=document,f='http://www.facebook.com/share',l=d.location,e=encodeURIComponent,p='.php?src=bm&v=4&i=1196353793&u='+e(l.href)+'&t='+e(d.title);1;try{if (!/^(.*\.)?facebook\.[^.]*$/.test(l.host))throw(0);share_internal_bookmarklet(p)}catch(z) {a=function() {if (!window.open(f+'r'+p,'sharer','toolbar=0,status=0,resizable=0,width=626,height=436'))l.href=f+p};if (/Firefox/.test(navigator.userAgent))setTimeout(a,0);else{a()}}void(0)''',
            'class': 'icon-facebook-sign'
        },
        'twitter': {
            'url': '''javascript:(function(){window.twttr=window.twttr||{};var D=550,A=450,C=screen.height,B=screen.width,H=Math.round((B/2)-(D/2)),G=0,F=document,E;if(C>A){G=Math.round((C/2)-(A/2))}window.twttr.shareWin=window.open('http://twitter.com/share','','left='+H+',top='+G+',width='+D+',height='+A+',personalbar=0,toolbar=0,scrollbars=1,resizable=1');E=F.createElement('script');E.src='http://platform.twitter.com/bookmarklets/share.js?v=1';F.getElementsByTagName('head')[0].appendChild(E)}());''',
            'class': 'icon-twitter'
        },
        'googleplus': {
            'url': '''javascript:void(window.open('https://plus.google.com/share?ur\l='+encodeURIComponent(location), 'Share to Google+','width=600,height=460,menubar=no,location=no,status=no'));''',
            'class': 'icon-google-plus-sign'
        },
        'linkedin': {
            'url': '''javascript:(function(){var%20d=document,l=d.location,f='http://www.linkedin.com/shareArticle?mini=true&ro=false&trk=bookmarklet&title='+encodeURIComponent(d.title)+'&url='+encodeURIComponent(l.href),a=function(){if(!window.open(f,'News','width=520,height=570,toolbar=0,location=0,status=0,scrollbars=yes')){l.href=f;}};if(/Firefox/.test(navigator.userAgent)){setTimeout(a,0);}else{a();}})()''',
            'class': 'icon-linkedin-sign'
        },
        # pinterest not ready yet
        # 'pinterest': {
        #     'url': '''javascript:void((function(d){var%20e=d.createElement('script');e.setAttribute('type','text/javascript');e.setAttribute('charset','UTF-8');e.setAttribute('src','//assets.pinterest.com/js/pinmarklet.js?r='+Math.random()*99999999);d.body.appendChild(e)})(document));''',
        #     'class': 'icon-pinterest'
        # },
    }

    sites = args.cmdstr.split('\n')
    for site in sites:
        page.addMessage(
            '''<a class="sharing-button" href="{url}"><i class="{class_}"></i></a>'''.format(
                url=share_info[site]['url'],
                class_=share_info[site]['class']))

    return params


def match(*whatever):
    return True
