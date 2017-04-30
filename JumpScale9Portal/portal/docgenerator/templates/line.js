    var line = new RGraph.Line("{lineId}", {lineData});
    
    line.Set('chart.title', '{lineTitle}');
    line.Set('chart.linewidth', 2);
    line.Set('chart.labels', {lineHeaders});
    line.Set('chart.key', {lineLegend});
    line.Set('chart.gutter.left', 90);
    
    line.Draw();
