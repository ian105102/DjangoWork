from django.shortcuts import render
from Stock.models import stock_data
from django.http import JsonResponse
import twstock

# Create your views here.


def get(request):
    t = 0
    stock_symbols = [
        "2330",
        "2317",
        "2454",
        "1301",
        "1303",
        "2412",
        "2308",
        "2881",
        "2891",
        "2892",
    ]
    for symbol in stock_symbols:
        stock = twstock.Stock(symbol)
        historical_data = stock.fetch_from(2023, 4)  # 2023/4/到現在

        for data in historical_data:
            stock_data.objects.update_or_create(
                stock_symbol=symbol,
                date=data.date,
                defaults={
                    "total_capacity": data.capacity,
                    "total_turnover": data.turnover,
                    "open_price": data.open,
                    "high_price": data.high,
                    "low_price": data.low,
                    "close_price": data.close,
                    "change_price": data.change,
                    "trans_action": data.transaction,
                },
            )
    t += 1
    data = {"message": "資料已成功存入資料庫"}
    return JsonResponse(data)


def home(request):

    try:
        # 變數 = 資料庫名稱.方法(條件)   .first()是指符合條件的第一筆  #還有其他拿資料的方法
        Stock_Symbol = request.GET.get("stock_symbol")
        unit = stock_data.objects.filter(
            stock_symbol=Stock_Symbol
        ).last()  # 讀取一筆資料

        # 打包到字典
        data_dict = {
            "2330": {
                "image": "image/2330.jpg",
                "title": "2330 臺灣積體電路",
                "description": "臺灣積體電路製造公司，簡稱TSMC、臺積電、臺積或臺積公司，為臺灣一家從事晶圓代工的公司。",
                "url": "?stock_symbol=2330",
            },
            "2317": {
                "image": "image/2317.png",
                "title": "2317 鴻海精密工業",
                "description": "鴻海精密工業是臺灣電子製造公司，也是鴻海科技集團的核心企業。",
                "url": "?stock_symbol=2317",
            },
            "2454": {
                "image": "image/2454.jpg",
                "title": "2454 聯發科技",
                "description": "聯發科技，簡稱聯發科，是臺灣一家為無線通訊、高畫質電視設計系統晶片的無廠半導體公司。",
                "url": "?stock_symbol=2454",
            },
            "1301": {
                "image": "image/1301.jpg",
                "title": "1301 台灣塑膠工業",
                "description": "台塑工業股份有限公司是一家位於台灣的塑膠公司，主要生產聚氯乙烯樹脂和其他塑膠產品。",
                "url": "?stock_symbol=1301",
            },
            "1303": {
                "image": "image/1303.jpg",
                "title": "1303 南亞塑膠",
                "description": "南亞塑膠工業股份有限公司簡稱南亞、南亞塑膠，是台灣一家塑膠公司，1958年創立。",
                "url": "?stock_symbol=1303",
            },
            "2412": {
                "image": "image/2412.jpg",
                "title": "2412 中華電信",
                "description": "中華電信是臺灣綜合電信服務業者之一，前身為交通部電信總局的營運部門。",
                "url": "?stock_symbol=2412",
            },
            "2308": {
                "image": "image/2308.jpg",
                "title": "2308 台達電子",
                "description": "台達電子工業股份有限公司，是一家臺灣的電子製造公司。",
                "url": "?stock_symbol=2308",
            },
            "2881": {
                "image": "image/2881.jpg",
                "title": "2881 富邦金融",
                "description": "富邦金融控股股份有限公司是一家臺灣的金融控股公司。",
                "url": "?stock_symbol=2881",
            },
            "2891": {
                "image": "image/2891.png",
                "title": "2891 中國信託",
                "description": "中國信託金融控股股份有限公司是臺灣的金融控股公司之一。",
                "url": "?stock_symbol=2891",
            },
            "2892": {
                "image": "image/2892.png",
                "title": "2892 第一金控",
                "description": "第一金融控股為臺灣的金融控股公司於2003年1月2日以第一商業銀行為主體，由股份轉換方式成立。",
                "url": "?stock_symbol=2892",
            },
        }
    except:
        print("Error")

    return render(request, "index.html", {"Data": data_dict})


def search(request):
    data_dict = {}
    # 強烈建議了解資料庫內部結構後再進行操作，例如下載DB.Browser可查看資料庫內容
    try:
        # 變數 = 資料庫名稱.方法(條件)   .first()是指符合條件的第一筆  #還有其他拿資料的方法
        Stock_Symbol = request.GET.get("stock_symbol")

        twstock.realtime.mock = False
        unit = twstock.realtime.get(Stock_Symbol)

        # unit = stock_data.objects.filter(
        #     stock_symbol=Stock_Symbol
        # ).last()  # 讀取一筆資料

        # 打包到字典
        data_dict = {
            "time": unit["timestamp"],
            "stock_symbol": unit["info"]["code"],
            "name": unit["info"]["name"],
            "fullname": unit["info"]["fullname"],
            "best_bit_price": unit["realtime"]["best_bid_price"],
            "best_bit_volume": unit["realtime"]["best_bid_volume"],
            "best_ask_price": unit["realtime"]["best_ask_price"],
            "best_ask_volume": unit["realtime"]["best_ask_volume"],
            "open": unit["realtime"]["open"],
            "high": unit["realtime"]["high"],
            "low": unit["realtime"]["low"],
        }

    except:
        print("Error")

        # 在HTML文件中使用的變數.KEY會映射出這邊的字典對應值
    return render(request, "get_stock.html", {"Data": data_dict})
