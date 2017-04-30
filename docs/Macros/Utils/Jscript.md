Jscript
=======

Macro used to inject javascript code.

Wiki
----

```
\{\{jscript:
 $(document).ready(function() {
   var button = $("<input type='button' value='Click Me'></input>");
   button.click(function() {
     alert('You clicked me');    
   });
   $(".span9").append(button);
 });
\}\}
```

Output
------
