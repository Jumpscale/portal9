BarChart Macro
--------------

This macro is used to add barcharts to your page

### Parameters

-   'title': The title of the chart
-   'rows': 2-D list of the data which will be viewed in the chart. Each
    row represents a type of bars.
-   'headers': The headers of a group of charts.
-   'width': The width of the chart, in pixels.
-   'height': The height of the chart, in pixels.
-   'showcolumns': The list of columns to be shown.
-   'columnAliases': Aliases for specific values.
-   'onclickfunction': The name of the Javascript function which will be
    called when the chart is clicked.

### Example

```
\{\{barchart:
title=Test
height=900
size=400
headers=HEADER 1,HEADER 2,HEADER 3,HEADER 4,HEADER 5,HEADER 6,HEADER 7,HEADER 8
data.1.legend=nr of accidents
data.1.data= 55, 20, 13, 32, 5, 1, 2, 10
data.2.legend=nr of death
data.2.data= 60, 3, 2, 9, 10, 20, 20, 10
data.3.legend=nr of felool
data.3.data= 60, 3, 2, 9, 100, 2000, 2000, 10000
\}\}
```

