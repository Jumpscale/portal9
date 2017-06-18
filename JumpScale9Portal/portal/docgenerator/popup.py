from js9 import j
from .form import Form


class Popup(Form):

    def __init__(self, id, submit_url, header='', action_button='Confirm',
                 form_layout='', reload_on_success=True, navigateback=False,
                 clearForm=True, showresponse=False, gridbinding=None):
        self.widgets = []
        self.id = id
        self.form_layout = form_layout
        self.header = header
        self.action_button = action_button
        self.submit_url = submit_url
        self.showresponse = showresponse
        self.reload_on_success = reload_on_success
        self.navigateback = navigateback
        self.clearForm = clearForm
        self.gridbinding = gridbinding

        import jinja2
        self.jinja = jinja2.Environment(variable_start_string="${", variable_end_string="}")

    def write_html(self, page):
        template = self.jinja.from_string('''
        <form role="form" method="post" action="${submit_url}" class="popup_form"
        {% for key, value in data.items() -%}
            data-${key}="${value}"
        {%- endfor %}
        {% if gridbinding -%}
            data-gridbinding-name="${gridbinding[0]}"
            data-gridbinding-value="${gridbinding[1]}"
        {%- endif %}
        >
            <div id="${id}" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="${id}Label" aria-hidden="true">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>
                    <div id="${id}Label" class="modal-header-text">${header}</div>
                  </div>
                  <div class="modal-body-container">
                    <div class="modal-body modal-body-error alert alert-danger padding-all-small padding-left-large">
                      Error happened on the server
                    </div>
                    <div class="modal-body modal-body-message alert alert-success padding-all-small padding-left-large">
                    </div>
                    <div class="modal-body modal-body-form">
                    {% for widget in widgets %}${widget}{% endfor %}
                    </div>
                  </div>
                  <div class="modal-footer">
                  <button class="btn btn-primary" data-loading-text="Loading...">${action_button}</button>
                    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
                  </div>
                </div>
            </div>
        </form>
        ''')
        data = {'clearform': j.data.serializer.json.dumps(self.clearForm),
                'reload': j.data.serializer.json.dumps(self.reload_on_success),
                'showresponse': j.data.serializer.json.dumps(self.showresponse),
                'navigateback': j.data.serializer.json.dumps(self.navigateback)}

        gridbinding = self.gridbinding or {}
        content = template.render(id=self.id, header=self.header, action_button=self.action_button,
                                  form_layout=self.form_layout, widgets=self.widgets, submit_url=self.submit_url,
                                  clearForm=self.clearForm, data=data, gridbinding=gridbinding)

        css = """
        .modal-header-text { font-weight: bold; font-size: 24.5px; line-height: 30px; }
        .model.body {
                overflow-wrap: break-word;
                word-wrap: break-word;

                /* Instead use this non-standard one: */
                word-break: break-word;

                /* Adds a hyphen where the word breaks, if supported (No Blink) */
                -ms-hyphens: auto;
                -moz-hyphens: auto;
                -webkit-hyphens: auto;
                hyphens: auto;
        }
        """
        if css not in page.head:
            page.addCSS(cssContent=css)

        jsLink = '/jslib/old/jquery.form/jquery.form.js'
        if jsLink not in page.head:
            page.addJS(jsLink)

        js = self.jinja.from_string('''$(function(){
            $(".modal-body-error, .modal-body-message").hide();
            var resetForm = function($form) {
                $form.find('.modal-body').hide();
                $form.find('.modal-body-form').show();

                //in case we reload we need to reset the form here
                $form.find("input,select,textarea").prop("disabled", false)
                $form.find('.modal-footer > .btn-primary').button('reset').show();

            };
            $('.popup_form').ajaxForm({
                beforeSubmit: function(formData, $form, options) {
                    this.popup = $form;
                    var extradata = $form.data('extradata');
                    if (extradata) {
                        for (var name in extradata) {
                            formData.push({'name': name, 'value': extradata[name]});
                        }
                    }

                    var gridid = $form.data('gridbinding-name');
                    if (gridid) {
                        gridid = '#' + gridid;
                        var name = $form.data('gridbinding-value');
                        var rows = $(gridid).DataTable().rows({ selected: true}).data() || [];
                        for (var i = 0; i < rows.length; i++) {
                            formData.push({'name': name, 'value': rows[i][0]});
                        }
                    }
                    $form.find('.modal-footer > .btn-primary').button('loading');
                    $form.find("input,select,textarea").prop("disabled", true)
                },
                success: function(responseText, statusText, xhr) {
                    var extracallback = this.popup.data('extracallback');
                    if (extracallback) {
                        extracallback();
                    }
                    if (this.popup.data('clearform') === true) {
                        this.popup.clearForm();
                    }
                    if (this.popup.data('showresponse') === true) {
                        resetForm(this.popup);
                        this.popup.find('.modal-footer > .btn-primary').hide();
                        this.popup.find('.modal-body-form').hide();
                        this.popup.find('.modal-body-message').show();
                        this.popup.find('.modal-body-message').text(responseText);
                        return;

                    } else {
                        this.popup.find('.modal').modal('hide');
                    }
                    if (this.popup.data('navigateback') === true) {
                        resetForm(this.popup);
                        window.location = document.referrer;
                    } else if (this.popup.data('reload') === true) {
                        resetForm(this.popup);
                        location.reload();
                    }
                },
                error: function(response, statusText, xhr, $form) {
                    if (response) {
                        var errortext = response.responseJSON || response.responseText;
                        try {
                            var eco = JSON.parse(errortext);
                            errortext = eco.backtrace || errortext;
                        } catch (e) {
                            // dont do anything just use errortext
                        }
                        this.popup.find('.modal-body-error').text(errortext);
                    }
                    if (response && (response.status == 400 || response.status == 409)){
                        this.popup.find("input,select,textarea").prop("disabled", false)
                        this.popup.find('.modal-footer > .btn-primary').button('reset').show();
                    } else {
                        this.popup.find('.modal-body-form').hide();
                        this.popup.find('.modal-footer > .btn-primary').hide();
                    }
                    this.popup.find('.modal-body-error').show();
                }
            });
            $('.popup_form').on('hidden.bs.modal', function () {
                resetForm($(this));
            });
        });''')

        js = js.render()

        page.addJS(jsContent=js, header=False)

        page.addMessage(content)
