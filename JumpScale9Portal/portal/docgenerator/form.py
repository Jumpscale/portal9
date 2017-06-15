from js9 import j

class Form:

    def __init__(self, id, submit_url, submit_method='post', header='', action_button='Confirm',
                 form_layout='', reload_on_success=True, navigateback=False, clearForm=True, showresponse=False):
        self.widgets = []
        self.id = id
        self.form_layout = form_layout
        self.header = header
        self.action_button = action_button
        self.submit_url = submit_url
        self.submit_method = submit_method
        self.showresponse = showresponse
        self.reload_on_success = reload_on_success
        self.navigateback = navigateback
        self.clearForm = clearForm

        import jinja2
        self.jinja = jinja2.Environment(variable_start_string="${", variable_end_string="}")

    def addButton(self, value, type, link=None, id=None):
        tag = 'a' if link else 'button'
        template = self.jinja.from_string('''
        <${tag} type="${type}" class="btn btn-primary" {% if id %}href="${id}"{%endif%} {% if link %}href="${link}"{%endif%}>${value}</${tag}>
        ''')
        content = template.render(type=type, value=value, link=link, tag=tag, id=id)
        self.widgets.append(content)

    def addText(self, label, name, required=False, type='text', value='', placeholder='', step=''):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <input type="${type}" value="${value}", class="form-control" name="${name}" {% if required %}required{% endif %} placeholder="${placeholder}" step="${step}">
              </div>
        ''')
        content = template.render(
            label=label,
            name=name,
            type=type,
            value=value,
            required=required,
            placeholder=placeholder,
            step=step)
        self.widgets.append(content)

    def addHiddenField(self, name, value):
        template = self.jinja.from_string('''
            <input type="hidden" class="form-control" name="${name}" value="${value}">
        ''')
        content = template.render(value=value, name=name)
        self.widgets.append(content)

    def addTextArea(self, label, name, required=False, placeholder=''):
        # {% if required %}required{% endif %} placeholder="${placeholder}"
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <textarea class="form-control" name="${name}"></textarea>
              </div>
        ''')
        content = template.render(label=label, name=name, required=required, placeholder=placeholder)
        self.widgets.append(content)



    def addCodeBlock(self, code, name='contents', template="python", path="", edit=True, exitpage=True, spacename='', pagename='', linenr=False,
                     linecolor="#eee", linecolortopbottom="1px solid black", wrap=True, wrapwidth=100, querystr=None, theme='monokai', autorefresh=False, page=None):
        """
        TODO: define types of templates supported
        @template e.g. python
        if path is given and edit=True then file can be editted and a edit button will appear on editor
        """
        # if codeblock no postprocessing(e.g replacing $$space, ...) should be
        # done

        if edit:
            page.processparameters['postprocess'] = False
        page.addJS("%s/old/codemirror/lib/codemirror.js" % page.liblocation)
        page.addCSS("%s/old/codemirror/lib/codemirror.css" % page.liblocation)
        page.addJS("%s/old/codemirror/mode/javascript/javascript.js" % page.liblocation)
        page.addCSS("%s/old/codemirror/theme/%s.css" % (page.liblocation, theme))
        #page.addCSS("%s/codemirror/doc/docs.css"% page.liblocation)
        page.addJS("%s/old/codemirror/mode/%s/%s.js" % (page.liblocation, template, template))
        CSS = """
<style type="text/css">
    .CodeMirror {
        height: auto;
        border: $linecolor;
        border-top: $linecolortopbottom;
        border-bottom: $linecolortopbottom
    }
    .CodeMirror-scroll {
        overflow-y: hidden;
        overflow-x: auto;
    }

</style>
"""
        CSS = CSS.replace("$linecolortopbottom", linecolortopbottom)
        CSS = CSS.replace("$linecolor", linecolor)

        page.head += CSS
        page._codeblockid += 1
        # rows=\"20\"
        TA = "<textarea id=\"code%s\" name=\"%s\" >" % (page._codeblockid, name)
        TA += code
        TA += "</textarea>"
        if path != "" and edit:
            TA += "<button class='btn btn-primary margin-top-large' type=\"submit\" onclick=\"copyText%s();\">Save.</button>" % page._codeblockid
        self.widgets.append(TA)

        if path != "" and edit:

            F = """
    <form id="hiddenForm$id" name="hiddenForm$id" method="post" action="/restmachine/system/contentmanager/wikisave">
    <input type="hidden" name="text" id="text" value="">
    <input type="hidden" name="cachekey" id="cachekey" value="$guid">
    </form>
            """
            F = F.replace("$id", str(page._codeblockid))
            guid = j.data.idgenerator.generateGUID()
            content = {'space': spacename, 'path': path, 'page': pagename, 'querystr': querystr}
            j.apps.system.contentmanager.dbmem.set(guid, content, 60)
            F = F.replace("$guid", guid)
            page.addMessage(F)

        # if not self._hasCodeblock:
        if linenr:
            linenr = "true"
        else:
            linenr = "false"
        JS = """
var editor$id = CodeMirror.fromTextArea(document.getElementById("code$id"),
    {
    lineNumbers: $linenr,
    theme: "elegant",
    readOnly: $readonly,
    theme: "$theme",
    autoRefresh: "$autorefresh",
    lineWrapping: $wrap,
    mode: "{template}",
    onCursorActivity: function() {
        editor$id.addLineClass(hlLine, null, null);
        hlLine = editor$id.addLineClass(editor$id.getCursor().line, null, "activeline");
        }
    }
);
var hlLine = editor$id.addLineClass(0, "activeline");

function copyText$id() {
    var text=editor$id.getValue()
    document.hiddenForm$id.text.value = text;
    document.forms["hiddenForm$id"].submit();
    }
"""

        JS = JS.replace("$id", str(page._codeblockid))
        JS = JS.replace("$linenr", linenr)
        JS = JS.replace("$wrap", str(wrap).lower())
        JS = JS.replace("$readonly", str(not edit).lower())
        JS = JS.replace("$theme", theme)
        JS = JS.replace("$autorefresh", str(autorefresh).lower())

        page.addJS(jsContent=JS.replace("{template}", template), header=False)
        page._hasCodeblock = True


    def addNumber(self, label, name, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <input type="number" class="form-control" name="${name}" {% if required %}required{% endif %}>
              </div>
        ''')
        content = template.render(label=label, name=name, required=required)
        self.widgets.append(content)

    def addDropdown(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <select class="form-control" name="${name}" {% if required %}required{% endif %}>
                    {% for title, value in options %}
                        <option value="${value}">${title}</option>
                    {% endfor %}
                </select>
              </div>
        ''')
        content = template.render(label=label, name=name, required=required, options=options)
        self.widgets.append(content)

    def addRadio(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height">${label}</label>
                {% for title, value in options %}
                    <label>
                        <input type="radio" name="${name}" value="${value}" {% if required %}required{% endif %}>
                            ${title}
                        </input>
                    </label>
                {% endfor %}
              </div>
        ''')
        content = template.render(label=label, name=name, options=options, required=required)
        self.widgets.append(content)

    def addCheckboxes(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height">${label}</label>
                {% for title, value, checked in options %}
                    <label class="checkbox">
                      <input type="checkbox" {% if checked %}checked{% endif%} {% if required %}required{% endif %} name="${name}" value="${value}" />
                      ${title}
                    </label>
                {% endfor %}
            </div>
        ''')
        content = template.render(label=label, name=name, options=options, required=required)
        self.widgets.append(content)

    def write_html(self, page):
        template = self.jinja.from_string('''
        <form class="form" role="form" method="${submit_method}" action="${submit_url}"
        {% for key, value in data.items() -%}
            data-${key}="${value}"
        {%- endfor %}
        >
            <div class="form-group">
                {% for widget in widgets %}${widget}{% endfor %}
             </div>

             <label id="form_response"></label>

        </form>
        ''')

        jsLink = '/jslib/old/jquery.form/jquery.form.js'
        if jsLink not in page.head:
            page.addJS(jsLink)

        js = self.jinja.from_string('''$(function(){
            var resetForm = function($form) {
                $form.find('.modal-body').hide();
                $form.find('.modal-body-form').show();

                //in case we reload we need to reset the form here
                $form.find("input,select,textarea").prop("disabled", false)
                $form.find('.modal-footer > .btn-primary').button('reset').show();

            };
            $('.form').ajaxForm({
                beforeSubmit: function(formData, $form, options) {
                    this.form = $form;
                    var extradata = $form.data('extradata');
                    if (extradata) {
                        for (var name in extradata) {
                            formData.push({'name': name, 'value': extradata[name]});
                        }
                    }
                    $form.find('.modal-footer > .btn-primary').button('loading');
                    $form.find("input,select,textarea").prop("disabled", true)
                },
                success: function(responseText, statusText, xhr) {
                    var extracallback = this.form.data('extracallback');
                    if (extracallback) {
                        extracallback();
                    }
                    if (this.form.data('clearform') === true) {
                        this.form.clearForm();
                    }
                    if (this.form.data('showresponse') === true) {
                        resetForm(this.form);
                        this.form.find('.modal-footer > .btn-primary').hide();
                        this.form.find('.modal-body-form').hide();
                        this.form.find('.modal-body-message').show();
                        this.form.find('#form_response').text(responseText).addClass('alert alert-success');
                        return;

                    } else {
                        this.form.find('.modal').modal('hide');
                    }
                    if (this.form.data('navigateback') === true) {
                        resetForm(this.form);
                        window.location = document.referrer;
                    } else if (this.form.data('reload') === true) {
                        resetForm(this.form);
                        location.reload();
                    }
                },
                error: function(response, statusText, xhr, $form) {
                    if (response) {
                        var responsetext = response.statusText || response.responseText;
                        this.form.find('#form_response').text(responsetext).addClass("alert alert-danger");
                    }
                    if (response && (response.status == 400 || response.status == 409)){
                        this.form.find("input,select,textarea").prop("disabled", false)
                        this.form.find('.modal-footer > .btn-primary').button('reset').show();
                    } else {
                        this.form.find('.modal-body-form').hide();
                        this.form.find('.modal-footer > .btn-primary').hide();
                    }
                }
            });
            $('.form_form').on('hidden.bs.modal', function () {
                resetForm($(this));
            });
        });''')

        js = js.render()

        page.addJS(jsContent=js, header=False)


        data = {'clearform': j.data.serializer.json.dumps(self.clearForm),
                'reload': j.data.serializer.json.dumps(self.reload_on_success),
                'showresponse': j.data.serializer.json.dumps(self.showresponse),
                'navigateback': j.data.serializer.json.dumps(self.navigateback)}
        content = template.render(id=self.id, header=self.header, action_button=self.action_button, form_layout=self.form_layout,
                                  widgets=self.widgets, submit_url=self.submit_url,
                                  submit_method=self.submit_method, clearForm=self.clearForm, data=data)

        page.addMessage(content)
