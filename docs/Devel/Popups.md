Popups
======

You can use the popup class to create Bootstrap modal forms from inside
your macro. This is an example of a macro & below it the expected output

```python
from JumpScale.portal.docgenerator.popup import Popup

def main(j, args, params, tags, tasklet):
    params.result = page = args.page

    pars = args.expandParamsAsDict()

    page.addMessage('<a href="#{0}" role="button" class="btn" data-toggle="modal">Launch demo modal {0}</a>'.format(pars['id']))

    popup = Popup(id=pars['id'], header='Text popup', submit_url=pars['submit_url'])
    popup.addHiddenField('hidden_field', 'hidden_value')
    popup.addText('First name', 'firstname', required=True)
    popup.addNumber('Age', 'age')
    popup.addDropdown('Choose licence', 'license', [('MIT', 'mit'), ('BSD', 'bsd'), ('GPL version 3', 'gpl3')])
    popup.addRadio('Choose licence', 'license2', [('MIT', 'mit'), ('BSD', 'bsd'), ('GPL version 3', 'gpl3')])
    popup.addCheckboxes('Choose the software', 'software', [('MS Office', 'msoffice'), ('Photoshop', 'photoshop')])
    popup.write_html(page)

    return params


def match(j, args, params, tags, tasklet):
    return True
```

This is the button which will show the popup. You can put it in your
macro if you want

Output
------
