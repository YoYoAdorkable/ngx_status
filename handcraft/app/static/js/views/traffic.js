$(function(){

    //convert Hex to RGBA
    function convertHex(hex,opacity){
        hex = hex.replace('#',''); r = parseInt(hex.substring(0,2), 16);
        g = parseInt(hex.substring(2,4), 16);
        b = parseInt(hex.substring(4,6), 16);

        result = 'rgba('+r+','+g+','+b+','+opacity/100+')';
        return result;
    }

    //Random Numbers
    function random(min,max) {
        return Math.floor(Math.random()*(max-min+1)+min);
    }

    //Main Chart
    function traffic() { 
    $.get("/traffic",function(result,status){
        var data1 = result['flow']['Inbound'];
        var data2 = result['flow']['Outbound'];
        //var data3 = result['code']['XX2'];
        //var data4 = result['code']['XX3'];
        //var data5 = result['code']['XX4'];
        //var data6 = result['code']['XX5'];

        var data = {
            labels: result['flow']['Timespan'],
            datasets: [
                {
                    label: 'Outbound',
                    backgroundColor: convertHex($.brandInfo,10),
                    borderColor: $.brandInfo,
                    pointHoverBackgroundColor: '#fff',
                    borderWidth: 2,
                    data: data2
                },
                {
                    label: 'Inbound',
                    backgroundColor: 'transparent',
                    borderColor: $.brandSuccess,
                    pointHoverBackgroundColor: '#fff',
                    borderWidth: 2,
                    data: data1
                }
            ]
        };


        var options = {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        drawOnChartArea: false,
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            elements: {
                point: {
                    radius: 0,
                    hitRadius: 10,
                    hoverRadius: 4,
                    hoverBorderWidth: 3,
                }
            },
        };
        var ctx = $('#traffic-chart');
        var mainChart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: options
        });
    

        //
        //var ctx = $('#code-chart');
        //var mainChart = new Chart(ctx, {
        //    type: 'line',
        //    data: code_data,
        //    options: options
        //});

        //

    });
    };
    traffic();
    setInterval(traffic,20000)
});
