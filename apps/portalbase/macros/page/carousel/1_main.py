
def main(j, args, params, tags, tasklet):

    page = args.page

    C = """
    <!-- Carousel
    ================================================== -->
    <div id="myCarousel" class="carousel slide">
      <div class="carousel-inner">
    """

    state = "start"
    first = True
    content = ""
    title = ""
    img = ""
    for line in args.cmdstr.split("\n"):
        # print line
        # print state
        # print "content:%s" % content
        # print "title:%s %s" % (title,img)

        if line.strip() == "" or line[0] == "#":
            continue

        if state == "section" and line.find("----") != -1:
            state = "start"
            # end of section fill in
            if first:
                C += "            <div class=\"item active\">\n"
                first = False
            else:
                C += "            <div class=\"item\">\n"
            C += "                <img src=\"%s\" alt="">" % img
            C2 = """
            <div class="container">
            <div class="carousel-caption">
              <h1>{title}</h1>
              <p class="lead">
              {content}
              </p>
            </div>
          </div>
          </div>
          """
            C2 = C2.replace("{title}", title)
            C2 = C2.replace("{content}", content)
            C += C2

            continue

        if state == "section":
            content += "%s\n" % line

        if state == "start" and line.find("|") != -1:
            state = "section"
            content = ""
            title, img = line.split("|")
            title = title.strip()
            img = img.strip()

    C2 = """
    </div>
      <a class="left carousel-control" href="#myCarousel" data-slide="prev">&lsaquo;</a>
      <a class="right carousel-control" href="#myCarousel" data-slide="next">&rsaquo;</a>
    </div><!-- /.carousel -->

    """
    C += C2

    page.addMessage(C)

    C = """
        !function ($) {
            $(function () {
                // carousel demo
                $('#myCarousel').carousel()
            })
        } (window.jQuery)
    """

    page.addJS(jsContent=C, header=False)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
