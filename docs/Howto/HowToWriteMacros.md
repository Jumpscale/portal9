How to Manipulate the Doc Content
=================================

Please see [Macros](Macros) page for explination about what macros are and what they can do.

```python
def main(j, args, params, tags, tasklet):
    doc = args.doc
    idd = int(args.getTag('id'))

    #get actor from appserver
    actor=j.apps.system.gridmanager
    
    #retrieve nods from actor method
    obj=actor.getNodes(id=idd)[0] #returns 1 node in array (is how the getNodes method works)
    #obj is a dict

    #apply the properties of the object as parameters to the active wiki document
    doc.applyTemplate(obj)

    #IMPORTANT return 2x doc (not (out,doc)) but return (doc,doc) this tells the appserver that the doc was manipulated
    params.result = (doc, doc)

    return params
```

example wiki page using this macro

```
@usedefaults

#next calls the above node macro & manipulates this wiki text, ${description}, ${name} will be replaced
#the node macro is called with get statement $$id, id is received from the query params out of the url
{{node: id:$$id}}

h2. ${name}

${description}
```

Its even possible to write [jinja2](http://jinja.pocoo.org/docs/dev/) inside your WIKI, base in mind this can be used only once so only one `macro` on the entire page should alls `doc.applyTemplate`.

Example


```
{{node: id:$$id}}

h2. ${name}
${description}
{% for ip in ipaddr %}
* ${ip}
{% endfor %}
```

For variables we use ${varname} notation since the default of Jinja2 is `{{varname}}` which conflicts with our macro syntax.