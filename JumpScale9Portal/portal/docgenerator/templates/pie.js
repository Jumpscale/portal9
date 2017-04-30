    var pie = new RGraph.Pie('{pieId}', {pieData});

    pie.Set('chart.title', '{pieTitle}');
    //pie.Set('chart.labels', {pieLegend});
    pie.Set('chart.shadow', true);
    pie.Set('chart.linewidth', 1);
    pie.Set('chart.exploded', 3);
    pie.Set('chart.key', {pieLegend});
    
    pie.Draw();

