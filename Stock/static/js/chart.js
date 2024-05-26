let Chart
(async () => {
    const ohlc = [],
        volume = [],
        dSeriesData = [], // 儲存 %D 值的數據
        kSeriesData = []; // 儲存 %K 值的數據
    const data = await fetch(
        'http://127.0.0.1:8000/Stock/get_chart/?stock_symbol='+stock_symbol
    ).then(response => response.json());
    console.log(data);
    // split the data set into ohlc and volume

        dataLength = data.length,
        // set the allowed units for data grouping
        groupingUnits = [[
            'week',                         // unit name
            [1]                             // allowed multiples
        ], [
            'month',
            [1]
        ]];

        for (let i = 0; i < dataLength; i += 1) {
            let stockData = data[i]; // 取得單個股票資訊物件
            const stockDate = new Date(stockData.date);
            stockDate.setDate(stockDate.getDate() + 1);
            const oneDayLaterTimestamp = stockDate.getTime();
            ohlc.push([
                oneDayLaterTimestamp, // 將日期轉換為時間戳記
                parseFloat(stockData.open_price),   // 開盤價
                parseFloat(stockData.high_price),   // 最高價
                parseFloat(stockData.low_price),    // 最低價
                parseFloat(stockData.close_price)   // 收盤價
            ]);
        
        
            volume.push([
                oneDayLaterTimestamp, // 將日期轉換為時間戳記
                parseInt(stockData.trans_action)    // 交易量
            ]);


            let date = oneDayLaterTimestamp;
            let d_value = parseFloat(stockData.d_value);
            let k_value = parseFloat(stockData.k_value);
     
            dSeriesData.push([date, d_value]);
            kSeriesData.push([date, k_value]);
        }




        
    // create the chart
    Highcharts.setOptions({
        lang: {
            months: ['一月', '二月', '三月', '四月', '五月', '六月', 
                     '七月', '八月', '九月', '十月', '十一月', '十二月'],
            shortMonths: ['1月', '2月', '3月', '4月', '5月', '6月', 
                          '7月', '8月', '9月', '10月', '11月', '12月'],
            weekdays: ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
            rangeSelectorZoom: '縮放',
            rangeSelectorFrom: '從',
            rangeSelectorTo: '到',
  
        }
    });
     Chart= Highcharts.stockChart('container', {

        rangeSelector: {
            buttons: [{
                type: 'month',
                count: 1,
                text: '日線'  // 1個月
            }, {
                type: 'year',
                count: 1,
                text: '月線'  // 1年
            },],
            selected: 1 // 預設選中的範圍為 1 年
        },
        title: {
            text: '股票價格走勢圖'
        },


        xAxis: {
            dateTimeLabelFormats: {
                day: '%m月%d日', // 日顯示格式為月日
                month: '%Y年%b', // 月份顯示格式為年月
                year: '%Y年'     // 年份顯示格式
            }
        },
        yAxis: [{
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: '開盤/收盤價'
            },
            height: '70%',
    
            resize: {
                enabled: true
            }
            
        },{
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: '交易量'
            },
           
            top: '80%',
            height: '10%',
            offset: 0,
 
        } ,{
            labels: {
                text: 'KD值',
                align: 'left',
                x:10
            },
            title: {
                text: 'KD值'
            },
            top: '50%',
            height: '20%',
            offset: 0,
        }],
        tooltip: {
            split: true,
            positioner: function(labelWidth, labelHeight, point) {
                var chart = this.chart,
                    posX = point.plotX + chart.plotLeft,
                    posY = point.plotY + chart.plotTop,
                    tooltipX,
                    tooltipY;
    
                // 確保工具提示在圖表內部
                tooltipX = posX + 10; // 在點的右側
                tooltipY = posY - labelHeight - 10; // 在點的上方
    
                // 如果超出圖表右邊緣，則翻轉顯示在點的左側
                if (tooltipX + labelWidth > chart.plotWidth) {
                    tooltipX = posX - labelWidth - 10;
                }
    
                // 如果超出圖表上邊緣，則翻轉顯示在點的下方
                if (tooltipY < chart.plotTop) {
                    tooltipY = posY + 10;
                }
    
                return {
                    x: tooltipX,
                    y: 0
                };
            },
            formatter: function () {
                var s = '<b>' + Highcharts.dateFormat('%Y年%m月%d日', this.x) + '</b>';
                this.points.forEach(function (point) {
                    if(point.series.name === '股價'){
                        s += '<br/>開盤價：' + point.point.open;
                        s += '<br/>最高價：' + point.point.high;
                        s += '<br/>最低價：' + point.point.low;
                        s += '<br/>收盤價：' + point.point.close;
                    }
                    s += '<br/>' + point.series.name + '：' + point.y;
                });
                return s;
            }
        },

        series: [
            {
                type: 'candlestick',
                name: '股價',
                data: ohlc,
                yAxis: 0,
                color: 'green',
                upColor:'red' ,
                dataGrouping: {
                    units: groupingUnits
                }
            },
            {
                type: 'column',
                name: '交易量',
                data: volume,
                yAxis: 1,
                color: 'green', 
                dataGrouping: {
                    units: groupingUnits
                }
            },        {
                yAxis: 2,
                type: 'line',
                name: 'K值',
                data: kSeriesData,
         
            }, 
            {   
                yAxis: 2,
                type: 'line',
                name: 'D值',    
                data: dSeriesData,  
      
            }],

        });
//  
// Highcharts.chart('container_kd', {
    
//     chart: {
//         type: 'line'
//     },
//     title: {
        
//         text: 'KD指標'
//     },
//     xAxis: {
//         type: 'datetime',
//         dateTimeLabelFormats: {
//             day: '%m月%d日', // 日顯示格式為月日
//             month: '%Y年%b', // 月份顯示格式為年月
//             year: '%Y年'     // 年份顯示格式
//         },
//         title: {
//             text: 'Date'
//         }
//     },
//     tooltip: {
//         split: true,
//         positioner: function(labelWidth, labelHeight, point) {
//             var chart = this.chart,
//                 posX = point.plotX + chart.plotLeft,
//                 posY = point.plotY + chart.plotTop,
//                 tooltipX,
//                 tooltipY;

//             // 確保工具提示在圖表內部
//             tooltipX = posX + 10; // 在點的右側
//             tooltipY = posY - labelHeight - 10; // 在點的上方

//             // 如果超出圖表右邊緣，則翻轉顯示在點的左側
//             if (tooltipX + labelWidth > chart.plotWidth) {
//                 tooltipX = posX - labelWidth - 10;
//             }

//             // 如果超出圖表上邊緣，則翻轉顯示在點的下方
//             if (tooltipY < chart.plotTop) {
//                 tooltipY = posY + 10;
//             }

//             return {
//                 x: tooltipX,
//                 y: 0
//             };
//         },
//         formatter: function () {
//             var s = '<b>' + Highcharts.dateFormat('%Y年%m月%d日', this.x) + '</b>';
//             this.points.forEach(function (point) {
//                 s += '<br/>' + point.series.name + '：' + point.y;
//             });
//             return s;
//         }
//     },
//     yAxis: {
//             labels: {
//                 align: 'right',
//                 x:30
//             },
//             title: {
//                 text: ' '
//             },
//             top: '40%',
//             height: '30%',
//             offset: 0,
//         },
//     series: [
//         {
//             yAxis: 0,
//             type: 'line',
//             name: 'K值',
//             data: kSeriesData,
     
//         }, 
//         {   
//             yAxis: 0,
//             type: 'line',
//             name: 'D值',    
//             data: dSeriesData,  
  
//         }],

//     });



})();



