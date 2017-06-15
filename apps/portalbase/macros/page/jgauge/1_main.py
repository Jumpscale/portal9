
def main(j, args, params, tags, tasklet):

    page = args.page

    page.addJS("/jslib/old/jgauge/excanvas.min.js")
    page.addJS("/jslib/old/jgauge/jQueryRotate.min.js")
    page.addJS("/jslib/old/jgauge/jgauge-0.3.0.a3.min.js")
    page.addCSS("/jslib/old/jgauge/jgauge.css")

    params = args.expandParams()

    paramsd = params.getDict()

    if "id" in paramsd:
        gaugeid = int(params.id)
    else:
        gaugeid = j.apps.system.contentmanager.dbmem.increment("jgaugeid")

    if "style" in paramsd:
        style = params.style.lower().strip()
    else:
        style = "black"  # default does also work

    if "height" in paramsd:
        height = params.height
    else:
        height = 114

    if "width" in paramsd:
        width = params.width
    else:
        width = 200

    if "start" in paramsd:
        start = params.start
    else:
        start = 0

    if "end" in paramsd:
        end = params.end
    else:
        end = 12

    if "labelsuffix" in paramsd:
        labelsuffix = str(params.labelsuffix)
    else:
        labelsuffix = ""

    if "randomspeed" in paramsd:
        randomspeed = str(params.randomspeed)
    else:
        randomspeed = 100

    C = """
var gauge$idval= $val
var myGauge$id = new jGauge();
myGauge$id.id = 'jGauge$id';
$gid.width = $width;
$gid.height = $height;
$gid.ticks.start = $start;
$gid.ticks.end = $end;

    """

    if style == "black":
        C = C.replace("$height", str(170))
        C = C.replace("$width", str(170))
        C += """
$gid.imagePath = '/jslib/old/jgauge/img/jgauge_face_taco.png';
$gid.segmentStart = -225
$gid.segmentEnd = 45
$gid.needle.xOffset = 0;
$gid.needle.yOffset = 0;
$gid.label.yOffset = 50;
$gid.needle.imagePath = '/jslib/old/jgauge/img/jgauge_needle_taco.png';
$gid.label.color = '#0ce';
$gid.autoPrefix = autoPrefix.si; // Use SI prefixing (i.e. 1k = 1000).
$gid.label.precision = 0; // 0 decimals (whole numbers).
$gid.label.suffix = '$suffix'; // Make the value label watts.
$gid.ticks.labelRadius = 45;
$gid.ticks.labelColor = '#0ce';
$gid.ticks.count = 7;
$gid.ticks.color = 'rgba(0, 0, 0, 0)';
$gid.range.color = 'rgba(0, 0, 0, 0)';
"""
        C = C.replace("$gid", "myGauge%s" % gaugeid)
    else:
        C += "myGauge%s.imagePath='/jslib/old/jgauge/img/jgauge_face_default.png'\n" % (gaugeid)
        C += "myGauge%s.needle.imagePath='/jslib/old/jgauge/img/jgauge_needle_default.png'\n" % (gaugeid)

    cmds = ["segmentStart", "segmentEnd", "needle.limitAction ", "needle.xOffset", "needle.yOffset",
            "label.xOffset", "label.yOffset", "label.prefix", "label.suffix", "label.precision", "ticks.count", "ticks.start", "ticks.end",
            "ticks.color ", "ticks.thickness", "ticks.radius", "ticks.labelPrecision", "ticks.labelRadius", "range.radius",
            "range.thickness ", " range.start ", "range.end ", "range.color"]
    for cmd in cmds:
        if cmd in list(paramsd.keys()):
            C = "myGauge%s.%s=%s\n" % (gaugeid, cmd, paramsd["%s" % cmd])

    C = C.replace("$id", str(gaugeid))
    C = C.replace("$height", str(height))
    C = C.replace("$width", str(width))
    C = C.replace("$start", str(start))
    C = C.replace("$end", str(end))
    C = C.replace("$gid", "myGauge%s" % gaugeid)
    C = C.replace("$suffix", labelsuffix)
    C = C.replace("$val", params.val)

    page.addJS(jsContent=C)

    page.addHTML("<div id=\"jGauge%s\" class=\"jgauge\"></div>" % gaugeid)
    # page.addNewLine()
    # page.addPageBreak()

    if "random" in paramsd:
        C = """
function randVal$id()
{
        var newValue;
        if (Math.random() > 0.8) // Allow needle to randomly pause.
        {
                rnd= (Math.random()-0.5) * $range ;
                newValue = gauge$idval + rnd;

                if (newValue >= myGauge$id.ticks.start && newValue <= myGauge$id.ticks.end)
                {
                        // newValue is within range, so update.
                        myGauge$id.setValue(newValue);
                }
        }
}"""
        range = params.random
        C = C.replace("$id", str(gaugeid))
        C = C.replace("$range", str(range))
        page.addJS(jsContent=C)

    C = "myGauge%s.init();\n" % gaugeid
    C += "myGauge%s.setValue(%s)\n" % (gaugeid, params.val)

    if "random" in paramsd:
        C += "setInterval('randVal%s()', %s);\n" % (gaugeid, randomspeed)
    page.addDocumentReadyJSfunction(C)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
