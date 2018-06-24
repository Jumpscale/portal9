var pie = new RGraph.Pie("{pieId}", {pieData});

pie.Set("chart.title", "{pieTitle}");
// pie.Set('chart.labels', {pieLegend});
pie.Set("chart.shadow", true);
pie.Set("chart.linewidth", 1);
pie.Set("chart.exploded", 3);
pie.Set("chart.variant", "{donut}");
pie.Set("chart.key", {pieLegend});
pie.Set("chart.key.position", "graph");

pie.Set("chart.colors", ['#BCD3EB', '#1B3B44', '#536270', '#6B93AB', '#F2F2F8', '#568E8B', '#E4DA9C', '#CE899E', '#265356', '#723642', '#B0B0AE', '#4F3244', '#8892B6'])
pie.Set('chart.tooltips.effect', 'fade');
pie.Set('chart.tooltips.event', 'onmousemove');
pie.Set('chart.tooltips', {tooltips});
pie.Set('chart.highlight.style', '3d'); // Defaults to 3d anyway; can be 2d or 3d


if (!RGraph.isIE8()) {
    pie.Set('chart.zoom.hdir', 'center');
    pie.Set('chart.zoom.vdir', 'up');
}

pie.Set('chart.strokestyle', 'white');
pie.Draw();