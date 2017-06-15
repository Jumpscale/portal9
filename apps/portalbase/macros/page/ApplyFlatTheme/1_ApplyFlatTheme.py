
def main(j, args, params, tags, tasklet):

    page = args.page
    params.extend(args)
    page.addBootstrap()
    page.addFavicon("/system/.files/img/favicon/png", 'image/png')
    page.addCSS('/jslib/flatui/css/flat-ui.css')
    page.addCSS('/jslib/new-ui/new-ui.css')
    page.addCSS('/jslib/new-ui/oocss.css')

    page.addJS('/jslib/pnotify/pnotify.js')
    page.addJS('/jslib/pnotify/pnotify.buttons.js')
    page.addJS('/system/.files/js/events.js')
    page.addCSS('/jslib/pnotify/pnotify.css')

    page.addJS(jsContent='''
        $( function () {
        $('body').addClass('flatTheme');

        $('link[href="/jslib/old/breadcrumbs/breadcrumbs.css"]').remove();
        $('link[href="/jslib/swagger/css/reset.css"]').remove();


        $('.nav-collapse.collapse').removeClass('nav-collapse').addClass('navbar-collapse');
        $('.btn.btn-navbar').replaceWith('<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".nav-collapse" aria-expanded="false">' +
            '<span class="sr-only">Toggle navigation</span>' +
            '<span class="icon-bar"></span>' +
            '<span class="icon-bar"></span>' +
            '<span class="icon-bar"></span>' +
          '</button>'
        );
        $('.brand').removeClass('brand').addClass('navbar-brand');
        $('.navbar-inner').addClass('navbar-form');
        $('.search-query').addClass('form-control');
        $('.newBreadcrumbArrow').removeClass('newBreadcrumbArrow separator').addClass('fui-arrow-right');

        $('.span1').removeClass('span1').addClass('col-md-1');
        $('.span2').removeClass('span2').addClass('col-md-2');
        $('.span3').removeClass('span3').addClass('col-md-3');
        $('.span4').removeClass('span4').addClass('col-md-4');
        $('.span5').removeClass('span5').addClass('col-md-5');
        $('.span6').removeClass('span6').addClass('col-md-6');
        $('.span7').removeClass('span7').addClass('col-md-7');
        $('.span8').removeClass('span8').addClass('col-md-8');
        $('.span9').removeClass('span9').addClass('col-md-9');
        $('.span10').removeClass('span10').addClass('col-md-10');
        $('.span11').removeClass('spa11').addClass('col-md-11');
        $('.span12').removeClass('span12').addClass('col-md-12');

        var toggles = document.querySelectorAll(".c-hamburger");
        for (var i = toggles.length - 1; i >= 0; i--) {
            var toggle = toggles[i];
            toggleHandler(toggle);
        };
        function toggleHandler(toggle) {
            toggle.addEventListener( "click", function(e) {
              e.preventDefault();
              (this.classList.contains("is-active") === true) ? this.classList.remove("is-active") : this.classList.add("is-active");
              $('.page-content').find('.sidebar-nav').toggleClass('hide');
              $('.page-content').find('.content').toggleClass('less-wide');
              $('.page-content').find('.navigation').toggleClass('wide-sidebar');
            });
        }
    });
     ''')

    page.addCSS('/system/.files/css/flatTheme.css')
    page.addCSS('/system/.files/css/default.css')

    params.result = page

    return params
