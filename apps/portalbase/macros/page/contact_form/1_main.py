import re


def main(j, args, params, tags, tasklet):
    # There are 2 possible ways to create a contact_form
    # 1. Use the default layout
    #    {{ contact_form }}
    #
    # 2. Customize the layout
    #    {{ contact_form: receiver_email=email@incubaid.com | custom }}
    #        {{div: class=line}}{{ text: name=email | required }}{{div}}
    #        {{div: class=line}}{{ textarea: rows: 20 | cols=30 | required }}{{div}}
    #        {{div: class=line}}{{ submit: value=Send | loading-text=Sending... }}{{div}}
    #        {{ submit: value=Send | loading-text=Sending... }}
    #        {{ reset }}
    #    {{ contact_form }}

    params.result = page = args.page

    smtp_server = args.tags.tagGet('smtp_server', '')
    smtp_login = args.tags.tagGet('smtp_login', '')
    smtp_password = args.tags.tagGet('smtp_password', '')
    if smtp_server and smtp_login and smtp_password:
        smtp_key = j.apps.system.contentmanager.dbmem.cacheSet(
            '', (smtp_server, smtp_login, smtp_password), 3600)  # 1 hour
    else:
        smtp_key = None

    if not getattr(page, 'tags_stack', None):
        page.tags_stack = []

    if args.tags.tagExists('receiver_email'):
        receiver_email = args.tags.tagGet('receiver_email')
        page.tags_stack.append('contact_form')
    elif page.tags_stack and page.tags_stack[-1] == 'contact_form':
        # This is the end of an existing custom contact_form, so I should close it
        page.addMessage('</form>')
        page.tags_stack.pop()
        return params
    else:
        page.addMessage('ERROR IN MACRO CONTACT_FORM: receiver_email is not set')
        return params

    subject_param = re.search(r'subject\s*:\s*([^\|\}]+)[\|\}]', args.macrostr)
    if subject_param:
        subject = subject_param.group(1)
    else:
        subject = 'About the website'

    page.addJS(jsLink='/jslib/old/jquery.form/jquery.form.js')
    js_content = '''
        $(function(){
            $('.contact_form').ajaxForm({
                clearForm: true,
                beforeSubmit: function() {
                    $('.contact_form').find('button').button('loading');
                    $('.contact_form').find('.alert').hide();
                },
                success: function(data) {
                    $('.contact_form').find('button').button('reset');
                    if (data.result.substr(0, 7).toLowerCase() === 'success') {
                        $('.contact_form').find('.alert').removeClass('alert-error').addClass('alert-success').text('Sent successfully.').show();
                    } else {
                        $('.contact_form').find('.alert').removeClass('alert-success').addClass('alert-error').text(data.result).show();
                    }
                },
                error: function() {
                    $('.contact_form').find('button').button('reset');
                    $('.contact_form').find('.alert').removeClass('alert-success').addClass('alert-error').text('Failed to send. Please try again later.').show();
                }
            });
        });
        '''
    if js_content not in page.head:
        page.addJS(jsContent=js_content)

    email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"

    page.addMessage('''
        <form class="form-horizontal contact_form" method="get" action="/restmachine/system/emailsender/send">
            <div class="alert" style="display: none"></div>
            <input type="hidden" name="smtp_key" value="{smtp_key}" />
            <input type="hidden" name="receiver_email" value="{receiver_email}" />
            <input type="hidden" name="format" value="json" />
            <input type="hidden" name="subject" value="{subject}" />
            <div style="display: none"><input type="text" id="honeypot" name="honeypot"></input></div>
            '''.format(smtp_key=smtp_key, receiver_email=receiver_email, subject=subject))

    custom = args.tags.labelExists('custom')
    if not custom:
        page.addMessage('''
                <div class="control-group"><input type="text" name="sender_name" placeholder="Your name" required /></div>
                <div class="control-group"><input type="email" name="sender_email" placeholder="Your email" required pattern="{email_pattern}" /></div>
                <div class="control-group"><textarea name="body" cols="30" rows="10" required></textarea></div>
                <button type="submit" class="btn btn-primary" data-loading-text="Sending...">Send</button>
                <a href="#" onclick="$(this).parents('form')[0].reset(); return false;">Reset</a>
            </form>
        '''.format(email_pattern=email_pattern))
        page.tags_stack.pop()

    return params


def match(j, args, params, tags, tasklet):
    return True
