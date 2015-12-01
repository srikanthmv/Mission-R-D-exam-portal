/**
 * Created with PyCharm.
 * User: tony
 * Date: 10/28/14
 * Time: 3:29 PM
 * To change this template use File | Settings | File Templates.
 */

function check_plot() {

//    $(document).ready(function () {
//
//        $.jqplot('chart1', [
//            [
//                [1, 2],
//                [3, 5.12],
//                [5, 13.1],
//                [7, 33.6],
//                [9, 85.9],
//                [11, 219.9]
//            ]
//        ]);
//    });
    $(document).ready(function () {
        var s1 = [100, 600, 700, 800];
       // var s2 = [400, 210, 690, 820];

        // Can specify a custom tick Array.
        // Ticks should match up one for each y value (category) in the series.
         var ticks = ['Test1', 'Test2', 'Test3', 'Test4'];

        var plot1 = $.jqplot('chart1', [s1], {
            seriesDefaults: {
                renderer: $.jqplot.BarRenderer,
                rendererOptions: {fillToZero: true}
            },
            series: [
                {label: 'Hotel'},
                {label: 'Event Regristration'},
                {label: 'Airfare'}
            ], axes: {
                // Use a category axis on the x axis and use our custom ticks.
                xaxis: {

                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks
                },
                // Pad the y axis just a little so bars can get close to, but
                // not touch, the grid boundaries.  1.2 is the default padding.
                yaxis: {
                    pad: 1.05,
                    tickOptions: {formatString: '$%d'}
                }
            }
        });
    });
}