DataTables use
--------------

Adds sorting & filteration capabilities to all the tables in this page

### Options

-   disable\_filters: By default, the macro adds filters for each field.
    Passing this parameter with value 'true' will not add field-specific
    filters. This parameter is optional & its default value is false

### Example

```
\{\{datatables_use: disable_filters:False\}\}

||col1||col2||col3||col4||
|something a|yes|city|938429374|
|something b|yes|city|938429374|
|asomething|yes|city|938429374|
|bsomething|no|city|4353454|
```

