    var bar = new RGraph.Bar('{chartId}', {chartData});
    
    bar.Set('chart.title', '{chartTitle}');
    bar.Set('chart.labels', {chartHeaders});
    bar.Set('chart.key', {chartLegend});
    // Set gutter wide enough to allow (very) big numbers in the y-axis labels
    bar.Set('chart.gutter.left', 90);
    bar.Set('chart.events.click', {onclickfunction});

    bar.Draw();
