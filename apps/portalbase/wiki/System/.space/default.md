<html>
<head>
	<link rel="stylesheet" href="/jslib/bootstrap/css/bootstrap-3-3-6.min.css">
	<link rel="stylesheet" href="/jslib/old/bootstrap/css/bootstrap-responsive.css">
	<link rel="stylesheet" href="/jslib/flatui/css/flat-ui.css">
	<link rel="stylesheet" href="/jslib/new-ui/new-ui.css">
</head>
<body style="background: #ECF0F1;">
<header class="container" style="padding: 0;">
<div>
<nav class="navbar navbar-inverse navbar-embossed" role="navigation">
<div class="navbar-header">
<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-collapse-01">
<span class="sr-only">Toggle navigation</span>
</button>
<a class="navbar-brand" href="#">Portal/Jumpscale8</a>
</div>
<div class="navbar-collapse" id="navbar-collapse-01">
<ul class="nav navbar-nav navbar-left" style="width: 80%;">
{{adminmenu}}{{find}}
{{menu:
Documentation:/Help
Incubaid:http://www.incubaid.com
}}
</ul>
</div><!-- /.navbar-collapse -->
</nav>
</div>
</header>
<div class="container" style="background: #fff;">
<div class="col-md-2 navigation">
{{navigation}}
</div>
<div class="col-md-10" markdown="1">
{% block body %}{% endblock %}
</div>
</div>
<footer class="container">
</footer>
<script src="/jslib/jquery/jquery-2.0.3.min.js"></script>
<script src="/jslib/flatui/js/flat-ui.min.js"></script>
</body>
</html>