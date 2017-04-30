/*
 * Convert a list of nested li's to a tree 
 */
jQuery.fn.pagetree = function(){
    // e.preventDefault() is important, to stop the event from propagating to the parent li's
    this.find('li:has(ul)').addClass('expanded').click(function(e) {
        $(this).toggleClass('collapsed').toggleClass('expanded').children('ul').toggle('fast');
        e.preventDefault();
        return false;
    });

    this.find('li:not(:has(ul))').click(function(e) {
        e.preventDefault();
        return false;
    });

    this.find('li > a').click(function(e) {
        location.href = $(this).attr('href');
        e.preventDefault();
        return false;
    });

    // Collapse all items, but keep the branch of the current page
    this.find('li:has(ul)').each(function(){
        // Search for href to current page. If it's not there, collapse it.
        var nephews = $(this).find('ul').find('a');
        var brothers = $(this).find('a');
        var links = nephews.add(brothers);
        for (var i = 0; i < links.length; i++) {
            if (links[i].href == location.href) {
                $(links[i]).parent().addClass('active-item');
                return;
            }
        }

        // Href to current page not found. Now click the page
        $(this).click();
    });

    // Highlight current item
    href = window.location.href;
    parts = href.split("/");
    currentPage = decodeURI(parts[parts.length -1]);
    menuitemsel = "li:has(a[href*='"+ currentPage +"']), li:has(a[href*='" + encodeURI(currentPage) + "'])";
    $("li a.active").removeClass("active-item");
    $(menuitemsel).addClass("active-item");
};