let data;
fetch(url_ + 'Stock/get_chart/?stock_symbol=' + stock_symbol)
.then(response => response.json())
.then(data_ => {
    // 在控製臺輸出獲取到的資料
    data = data_;

    showChart(data)
    // 在這裡可以執行你想要做的操作，例如更新網頁上的圖表或顯示資料
})



function fetchHistoricalData(chartType, year, month) {
    const stockSymbol = "{{ Data.stock_symbol }}";

    let url = url_ + 'Stock/get_chart/?stock_symbol=' + stock_symbol
    if (chartType === 1) {
        url += `&year=${year}`;
    } else if(chartType === 2) {
        url += `&year=${year}&month=${month}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Process and display the chart data here
            showChart(data);

        });
}

var kdj = null;
var candle_pane = null;

// 圖表
function showChart(data) {
    document.getElementById('chart_image').style.height = '800px';
    document.getElementById('chart_image').style.width = '100%';


    let element = document.getElementById("chart_image");
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }

    var new_chart = document.createElement("div");
    new_chart.id = "chart_image_show";
    new_chart.style.height = '800px';
    //     new_chart.style.height = '80%' ;
    element.appendChild(new_chart);
    // 初始化
    var chart = klinecharts.init('chart_image_show')
    // 移除
    if (candle_pane != null)
        chart.removeIndicator(candle_pane);
    if (kdj != null)
        chart.removeIndicator(kdj);
    // 建主要K線
    candle_pane = chart.createIndicator('MA', false, {id: 'candle_pane'})

    // 建 KD
    kdj = chart.createIndicator('KDJ', "KDJ")
    // 載數據
    let chartDataList = Object.values(data);

    chart.applyNewData(chartDataList);

}