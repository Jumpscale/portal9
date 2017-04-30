
def main(j, args, params, tags, tasklet):

    page = args.page

    C = """
<style type="text/css">
<!--
.toggleItemstyle {font-family: Verdana, Arial, Helvetica, sans-serif; font-size:18px}
-->
</style>
    """
    page.addHTMLHeader(C)

    C = """
function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}
var inits = new Array();
for (i=0;i<50;i++) inits[i] = true;
var ons = new Array();
var offs = new Array();

function swap(img_id) {
    if (inits[img_id]) {
        inits[img_id] = false;
        MM_swapImage(img_id,'','/system/.files/toggle/toggle_on.gif',1);
        window.frames['code1'].location = "$on";
    }
    else {
        inits[img_id] = true;
        MM_swapImage(img_id,'','/system/.files/toggle/toggle_off.gif',1);
        window.frames['code1'].location = "$off";
    }
}
    """

    args = args.tags.getValues(nodeid=None, cmdipaddr="127.0.0.1", title="", port="0", value="off")

    nodeid = args["nodeid"]
    ip = args["cmdipaddr"]
    url = "http://" + ip + ":8001/rest/boatomatic/snapmanager"
    on = "%s/turnPortOn?key=1234&nodeid=%s&port=$port&format=text;" % (url, nodeid)
    off = "%s/turnPortOff?key=1234&nodeid=%s&port=$port&format=text;" % (url, nodeid)

    C = C.replace("$on", on)
    C = C.replace("$off", off)
    C = C.replace("$port", args["port"])

    page.addJS(jsContent=C)

    id = str(j.apps.system.contentmanager.dbmem.increment("toggleid"))

    # C="""
    # <td width="30%"><div align="left" class="toggleItemstyle">$title</div></td>
    # <td width="70%"><a href="#" align="left"  onClick="swap('$id')"><img src="/system/.files/toggle/toggle_off.gif"  name="$id" width="66" height="29" border="0" id="$id" /></a></td>
    # """

    title = args["title"]
    value = args["value"]

    if title != "":

        C = """
        <div align="left" class="toggleItemstyle">$title
            <a href="#" onClick="swap('$id')"><img src="/system/.files/toggle/toggle_$value.gif" name="$id" width="66" height="29" border="0" id="$id" valign="middle"/></a>
        </div>
        """

    else:

        C = """
        <div align="left" class="toggleItemstyle">
            <a href="#" onClick="swap('$id')"><img src="/system/.files/toggle/toggle_$value.gif" align="left" name="$id" width="66" height="29" border="0" id="$id" /></a>
            </div>
        """

    C = C.replace("$id", id)
    C = C.replace("$value", value)
    C = C.replace("$title", title)

    page.addMessage(C)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
