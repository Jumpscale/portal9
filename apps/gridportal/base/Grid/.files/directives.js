angular.module('jumpscale')
    .directive('chart', function ($timeout, $http) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {

            var timeoutId;
            var selectedStatistic = attrs.ngStat;
            scope.statisticsData = [];


            var updateChart = function(data, series){
                if (scope.plot){scope.plot.destroy();}
                element.empty();
                if (!data) {return;};
                scope.plot = $.jqplot(attrs.id, data, {
                    legend:{
                        show:true, 
                        placement: 'outside', 
                        renderer: $.jqplot.EnhancedLegendRenderer,
                        location:'n'
                    },
                    axesDefaults: {
                        tickRenderer: $.jqplot.CanvasAxisTickRenderer ,
                        tickOptions: {
                            fontSize: '10pt'
                        }
                    },
                    axes:{
                        xaxis:
                            {
                                renderer:$.jqplot.DateAxisRenderer,
                                tickOptions: {
                                    formatString: '%T',
                                    angle: -30
                                }
                            },
                        yaxis:
                            {
                            tickOptions:{
                                formatString:'%.2f'
                            }
                        }
                    },
                    cursor: {
                        show: true,
                        zoom:true
                    },
                    series: series
                });
            }
  
            function scheduleUpdate() {
                $http.get(attrs.ngUrl).
                    then(
                        function(result){
                            if ('series' in result.data[selectedStatistic][1]){
                                var series = result.data[selectedStatistic][1].series;
                                result.data[selectedStatistic][1].series = null;
                            }
                            var now = new Date().getTime();
                            for (var i = 0; i < result.data[selectedStatistic][0].length; i++) {
                                if(typeof scope.statisticsData[i] === 'undefined'){
                                    scope.statisticsData[i] = []
                                };
                                scope.statisticsData[i].push([now, result.data[selectedStatistic][0][i]]);
                            }
                            while (scope.statisticsData[0].length > 90){
                                scope.statisticsData[0].shift();
                            }
                            updateChart(scope.statisticsData, series); // update DOM
                        });

                // save the timeoutId for canceling
                timeoutId = $timeout(function() {
                    scheduleUpdate(); // schedule the next update
                    }, 5000);
            }
 
            element.on('$destroy', function() {
                $timeout.cancel(timeoutId);
            });
 
            // start the UI update process.
            scheduleUpdate();

        },
        scope:{}
        }
    }
        )
;
  