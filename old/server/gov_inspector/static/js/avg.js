$(document).ready(function () {
    // Returns a Google-Vis data-table filled with the ministries' average information.
    function loadData() {
        // Loads data from open-data server.
        var data = example_data;  // FIXME: DEVELOPMENT ONLY!
        var length = data.length;

        // Set up a Google-Vis data-table.
        var dataTable = new google.visualization.DataTable();

        dataTable.addColumn('string', 'משרד');
        dataTable.addColumn('number', 'עמידה ביעדים');

        dataTable.addRows(length);

        // Fill data.
        $.each(data, function (i, ministry) {
            dataTable.setValue(i, 0, ministry.name);
            dataTable.setValue(i, 1, ministry.avg);
        });

        return dataTable;
    }

    // Receives a Google-Vis data-table, and a DOM element, and draws the table as a bar chart @ the given element.
    function drawAvgChart(dataTable, htmlElement) {
        var chart = new google.visualization.BarChart(htmlElement);

        // Calculate average for each ministry.
        /*$.each(dataTable.F, function (i, ministry) {  // FIXME: Do this in GVis instead.
            ministry.c[1].v /= 2;  // FIXME: Calc is wrong.
        });*/

        // See [Google Vis docs](http://code.google.com/apis/chart/interactive/docs/gallery/barchart.html) for more info.
        chart.draw(dataTable, {
            width           : '100%',
            height          : 1000,
            legend          : 'none',
            backgroundColor : '#DEECF9',
            vAxis           : {
                direction : 1,
                textStyle : { fontSize : 20 }
            },
            hAxis           : {
                textStyle : { fontSize : 14 },
                format    : '0%',
                maxValue  : 1
            }
        });
    }

    // Called when Google-Vis API finishes loading.
    function init() {
        var dataTable = loadData();
        drawAvgChart(dataTable, document.getElementById('avg'));
    }

    google.setOnLoadCallback(init);
});

