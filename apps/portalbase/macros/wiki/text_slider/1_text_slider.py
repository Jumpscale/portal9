import re


def main(j, args, params, tags, tasklet):
    params.merge(args)

    out = '''{{css:/jslib/bootstrap/css/bootstrap.css}}
{{html:<script src="/jslib/bootstrap/js/bootstrap.js"></script>}}

{{cssstyle:
.carousel-caption{
    color:#000;
    position:static;
    min-height: 150px;
}
.carousel h2 { color: white; }
.carousel li.active { display: inline-block; }

.carousel-control { border: none; height: inherit; margin-top: inherit; background: inherit; }
}}
{{html:
<script>
$(function() {
    var captions = $('.carousel-caption').clone().css({'visibility': 'hidden', 'position': 'absolute', 'display': 'none'}).appendTo('body');
    var maxHeight = Math.max.apply(null, captions.map(function() { return $(this).height(); }));
    captions.remove();
    $('.carousel-caption').height(maxHeight + $('.carousel-indicators').height() + 10);
});
</script>
}}
'''

    slides = re.split('-{2,}', params.cmdstr)

    opening = '''
    {{html:
    <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
  <!-- Indicators -->
  <ol class="carousel-indicators">
  }}
  '''

    indicators = '\n'.join('''{{html:
        <li data-target="#carousel-example-generic" data-slide-to="%i"></li>
    }}''' % i for i, _ in enumerate(slides))

    opening2 = '''
    {{html:
  </ol>

  <!-- Wrapper for slides -->
  <div class="carousel-inner">
    <div class="item active">
      <div class="carousel-caption">
    }}
    '''

    separator = '''
    {{html:
    </div>
    </div>
    <div class="item">
      <div class="carousel-caption">
    }}
    '''

    closing = '''
    {{html:
    </div>
    </div>
  </div>

  <!-- Controls -->
  <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>
</div>
    }}'''

    out += opening + indicators + opening2 + separator.join(slides) + closing

    params.result = (out, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
