from js9 import j


class HTMLGalleria:

    def __init__(self, page, online=False):
        self.page = page
        if online:
            self.liblocation = "https://bitbucket.org/incubaid/jumpscale-core-6.0/raw/default/extensions/html/lib"
        else:
            # self.liblocation=j.sal.fs.joinPaths(j.tools.docgenerator.pm_extensionpath,"lib/datatables/")
            self.liblocation = "/jslib"

        self.page.addBootstrap()

    def addImagesFromBucket(self, bucketname, subfolder="lowdef   "):

        C = """
$(document).ready(function() {
    $('#example').dataTable( {
        "sDom": "<'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'span6'p>>",
        "bProcessing": false,
        "bServerSide": false,
        "sAjaxSource": "$url"
    } );
    $.extend( $.fn.dataTableExt.oStdClasses, {
        "sWrapper": "dataTables_wrapper form-inline"
    } );
} );"""
        C = C.replace("$url", url)
        self.page.addJS(jsContent=C, header=False)

#<table cellpadding="0" cellspacing="0" border="0" class="display" id="example">
# <table class="table table-striped table-bordered" id="example" border="0" cellpadding="0" cellspacing="0" width="100%">

        C = """
<div id="dynamic">
<table class="table table-striped table-bordered" id="example" border="0" cellpadding="0" cellspacing="0" width="100%">
    <thead>
        <tr>
$fields
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="5" class="dataTables_empty">Loading data from server</td>
        </tr>
    </tbody>
</table>
</div>"""

        fieldstext = ""
        for name in fieldnames:
            fieldstext += "<th>%s</th>\n" % (name)
        C = C.replace("$fields", fieldstext)

        self.page.addMessage(C, isElement=True, newline=True)
        return self.page

    def prepare4DataTables(self):

        self.page.addDocumentReadyJSfunction("$('.dataTable').dataTable();")
        self.page.functionsAdded["datatables"] = True
        return self.page
