
def main(j, args, params, tags, tasklet):
    page = args.page
    params.merge(args)
    page.addCSS(cssContent='''
.admin-menu{
	color: #fff;
}
.login-url{
	background-color: #1abc9c;
	margin-left: 15px !important;
}
.login-url:hover a{
	color: #fff !important;
}
''')
    spaceName = args.doc.getSpaceName()
    pageName = args.doc.name.split('.')[0]
    if j.portal.tools.server.active.isAdminFromCTX(params.requestContext):
        page.addMessage('''
	<ul class="nav navbar-nav navbar-left">
	<li class="dropdown">
	<a href="#" class="dropdown-toggle" data-toggle="dropdown">Navigation <b class="caret"></b></a>
	<ul class="dropdown-menu mega-menu">
	<li><a href="/system/create">New page</a></li>
	<li><a href="/system/editmarkdown?space={spaceName}&page={pageName}">Edit Page</a></li>
	<li><a href="/system/createspace">Create Space</a></li>
	<li class="divider"></li>
	<li><a href="/system/files?space={spaceName}">Files</a></li>
	<li class="divider"></li>
	<li><a href="/system/login?user_logoff_=1">Logout</a></li>
	<li><a href="/system/OverviewAccess?space={spaceName}">Access</a></li>
	<li><a onclick="{{ $.ajax({{'url': '/system/ReloadSpace?name={spaceName}'}}).done(function(){{  location.reload()}});void(0) }}" href="#">Reload</a></li>
	<li><a onclick="reloadAll();void 0;" href="#">ReloadAll</a></li>
	<li><a onclick="pullUpdate('{spaceName}');void 0;" href="#">Pull latest changes & update</a></li>
	<li class="divider"></li>
	<li><a href="/">Spaces</a></li>
	</ul>
	</li>
	</ul>
	'''.format(spaceName=spaceName, pageName=pageName))
        page.addJS("/jslib/old/adminmenu/adminmenu.js")
    else:
        page.addMessage('''
			<ul class="nav navbar-nav navbar-right login-url">
				<li><a href="/system/login?user_logoff_=1">Login</a></li>
			</ul>
		'''.format(spaceName=spaceName))

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
