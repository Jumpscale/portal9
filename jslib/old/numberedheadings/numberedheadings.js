jQuery.fn.numberedHeadings = function() {
    var segments = [];

    $(':header').each(function() { 
        var level = parseInt(this.nodeName.substring(1), 10);

        if(segments.length == level) {
            segments[level-1]++;
        } else if(segments.length > level) {
            segments = segments.slice(0, level);
            segments[level-1]++;
        } else if(segments.length < level) {
            for(var i = 0; i < (level-segments.length); i++) {
                segments.push(1);
            }
        }

        $(this).text(segments.join('.') + '. ' + $(this).text());
    });
}
