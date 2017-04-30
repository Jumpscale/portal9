Document Converter
==================

Uses Microsoft Office API to convert Powerpoint presentations, Word
documents and Excel worksheets to other formats.

To use:
-------

-   example url:
    <http://127.0.0.1/rest/office/converter/convertinputpath=https://www.eff.org/files/EFF_Social_Network_Law_Enforcement_Guides.xls&outtype=pdf&format=text>
-   parameters
    -   inputpath: path on filesystem or url. Must end with proper file
        extension. (In this case, xls)
    -   outtype: output type. Filetype extension desired. Defaults to
        pdf.
    -   username: optional. For file access.
    -   password: optional. For file access.
    -   outputdirectory: optional. Default is under
        **docconverter/base/office/.files/**

Currently supported:

-   *Powerpoint Presentation*
    -   Supported extensions: *.ppt*, *.pptx*
    -   Supported outtypes: *pdf, ppt*
-   *Word Documents*
    -   Supported extensions: *.doc*, *.docx*
    -   Supported outtypes: *html, rtf, xml, xps, pdf*
-   *Excel Worksheets*
    -   Supported extensions: *.xls,*.xlsx\_
    -   Supported outtypes: \_csv, html, xlsb, xlsx, xlsm, xls, txt,
        prn, pdf\_

