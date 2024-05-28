from django.shortcuts import render
from Stock.models import stock_data , stock_info
from django.http import JsonResponse
import twstock
from django.views.decorators.http import require_GET
from datetime import datetime
# Create your views here.




def get(request):
    stock_symbols = [       ## 這裡是股票代號
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

        # 創建或獲取 stock_info 物件
        stock_info_record, created = stock_info.objects.get_or_create()

        if created or not stock_info_record.stock_renew_date:
            # 若是新記錄或沒有更新日期，設置一個默認的起始日期
            start_year = 2023
            start_month = 4
        else:
            # 從上次更新日期開始
            last_update = datetime.strptime(stock_info_record.stock_renew_date, '%Y-%m-%d')
            start_year = last_update.year
            start_month = last_update.month
        
        historical_data = stock.fetch_from(start_year, start_month) ## 這裡是從twstock中取出歷史資料

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

        # 更新 stock_info 的更新日期到最新的日期
    if historical_data:                                             ## 如果有歷史資料
        last_date = historical_data[-1].date.strftime('%Y-%m-%d')   ## 取出最後一筆資料的日期
        stock_info_record.stock_renew_date = last_date              ## 將最後一筆資料的日期存入stock_info_record
        stock_info_record.save()                                    ## 儲存stock_info_record

    data = {"message": "資料已成功存入資料庫"}
    return JsonResponse(data)



def home(request):

    try:
        # 變數 = 資料庫名稱.方法(條件)   .first()是指符合條件的第一筆  #還有其他拿資料的方法
        Stock_Symbol = request.GET.get("stock_symbol")  # 取得網址中的參數
        unit = stock_data.objects.filter(
            stock_symbol=Stock_Symbol
        ).last()  # 讀取一筆資料

        # 打包到字典
        data_dict = {   ## 這裡是將資料打包到字典中
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
    error_message = None 

    try:
        Stock_Symbol = request.GET.get("stock_symbol")

        twstock.realtime.mock = False
        unit = twstock.realtime.get(Stock_Symbol)
        
        first_date = stock_data.objects.order_by('date').values_list('date', flat=True).first()
        # 獲取最後一個日期
        last_date = stock_data.objects.order_by('-date').values_list('date', flat=True).first()

        # 去除時間部分
        first_date = first_date.split()[0]
        last_date = last_date.split()[0]

        # 轉換為 datetime 對象
        first_date = datetime.strptime(first_date, '%Y-%m-%d')
        last_date = datetime.strptime(last_date, '%Y-%m-%d')

        # 提取年份和月份
        first_year = first_date.year
        last_year = last_date.year
        first_month = first_date.month
        last_month = last_date.month

        # 生成所有的年份和月份
        all_year = [i for i in range(first_year, last_year + 1)]
        all_month = {i: [j for j in range(1, 13)] for i in all_year}
        all_month[first_year] = [i for i in range(first_month, 13)]
        all_month[last_year] = [i for i in range(1, last_month + 1)]
        # unit = stock_data.objects.filter(
        #     stock_symbol=Stock_Symbol
        # ).last()  # 讀取一筆資料
        # 打包到字典
        time = datetime.utcfromtimestamp(unit['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        stock_symbol = unit["info"]["code"]
        name = unit["info"]["name"]         
        fullname = unit["info"]["fullname"]
        best_bit_price = [str(price).rstrip('0').rstrip('.') if '.' in str(price) else str(price) for price in unit["realtime"]["best_bid_price"]]
        best_bit_volume = list(map(str, unit["realtime"]["best_bid_volume"]))       
        best_ask_price = [str(price).rstrip('0').rstrip('.') if '.' in str(price) else str(price) for price in unit["realtime"]["best_ask_price"]]
        best_ask_volume = list(map(str, unit["realtime"]["best_ask_volume"]))       ## 這裡是取出best_ask_volume的值map()是對best_ask_volume的值進行轉換成str
        open_price = str(unit["realtime"]["open"]).rstrip('0').rstrip('.') if '.' in str(unit["realtime"]["open"]) else str(unit["realtime"]["open"])   ## rstrip()是去掉右邊的0和.  ## 如果有小數點，就去掉小數點
        high_price = str(unit["realtime"]["high"]).rstrip('0').rstrip('.') if '.' in str(unit["realtime"]["high"]) else str(unit["realtime"]["high"])   
        low_price = str(unit["realtime"]["low"]).rstrip('0').rstrip('.') if '.' in str(unit["realtime"]["low"]) else str(unit["realtime"]["low"])
        
        stock_back = Stock_Symbol in ["2330", "2317", "2454", "1301", "1303", "2412", "2308", "2881", "2891", "2892"]
        
       
        
        data_dict = {                   ## 這裡是將資料打包到字典中
            "time": time,
            "stock_symbol":  stock_symbol,
            "name":  name,
            "fullname": fullname,
            "best_bit_price": best_bit_price,
            "best_bit_volume": best_bit_volume,
            "best_ask_price":  best_ask_price,
            "best_ask_volume": best_ask_volume,
            "open": open_price,
            "high": high_price,
            "low":low_price,
            "last_date": last_date,
            "first_date": first_date,
            "all_month": all_month, 
            "all_year": all_year,
            "stock_back": stock_back,
        }

    except Exception as e:
        print("Error: ", e)
        error_message = "查無此資料"

        # 在HTML文件中使用的變數.KEY會映射出這邊的字典對應值
    return render(request, "get_stock.html", {"Data": data_dict ,"error_message": error_message} )

def calculate_kd(data):
    # 計算KD指標
    high_prices = [item['high_price'] for item in data]     ## 這裡是從data中取出high_price的值
    low_prices = [item['low_price'] for item in data]       ## 這裡是從data中取出low_price的值
    close_prices = [item['close_price'] for item in data]   ## 這裡是從data中取出close_price的值 

    k_values = []   ## 這裡是用來存放K值
    d_values = []   ## 這裡是用來存放D值

    for i in range(len(data)):
        if i < 8:  # KD指標需要9天的數據
            k_values.append(None)
            d_values.append(None)
            continue

        highest_high = max(high_prices[i - 8:i + 1])    ## 這裡是取出最高價
        lowest_low = min(low_prices[i - 8:i + 1])       ## 這裡是取出最低價
        current_close = close_prices[i]

        rsv = (current_close - lowest_low) / (highest_high - lowest_low) * 100  ## 這裡是計算RSV值
        if i == 8:
            k_values.append(rsv)        ## 這裡是將RSV值加入到K值中
            d_values.append(rsv)        ## 這裡是將RSV值加入到D值中
        else:
            k_values.append((k_values[-1] * 2 / 3) + (rsv / 3))                  ## 這裡是計算K值    
            d_values.append((d_values[-1] * 2 / 3) + (k_values[-1] / 3))        ## 這裡是計算D值
    return k_values, d_values


def get_chart(request):
    stock_symbol = request.GET.get('stock_symbol')
    year = request.GET.get('year')
    month = request.GET.get('month')

    if not stock_symbol:
        return JsonResponse({'error': 'Stock symbol is required'}, status=400)  ## 如果沒有股票代號，返回錯誤訊息

    if year and not month:
        try:
            year = int(year)
            start_date = datetime(year, 1, 1)       ## start_date是該年的1月1號
            end_date = datetime(year + 1, 1, 1)     ## end_date是下一年的1月1號
            data = stock_data.objects.filter(       ## 這裡是從資料庫中找出符合條件的資料
                stock_symbol=stock_symbol,          ## stock_symbol是股票代號
                date__gte=start_date,               ## date__gte是指日期大於等於start_date
                date__lt=end_date                   ## date__lt是指日期小於end_date
            )
        except ValueError:
            return JsonResponse({'error': 'Year must be an integer'}, status=400)   ## 如果年份不是整數，返回錯誤訊息
    elif year and month:
        try:
            year = int(year)
            month = int(month)
            start_date = datetime(year, month, 1)       ## start_date是該年的該月1號
            if month == 12:                             ## 如果是12月
                end_date = datetime(year + 1, 1, 1)     ## end_date是下一年的1月1號
            else:                                       ## 如果不是12月                    
                end_date = datetime(year, month + 1, 1) ## end_date是該年的下一個月1號
            data = stock_data.objects.filter(           ## 這裡是從資料庫中找出符合條件的資料
                stock_symbol=stock_symbol,              ## stock_symbol是股票代號
                date__gte=start_date,                    ## date__gte是指日期大於等於start_date 
                date__lt=end_date                       ## date__lt是指日期小於end_date
            )   
        except ValueError:
            return JsonResponse({'error': 'Year and month must be integers'}, status=400)   ## 如果年份和月份不是整數，返回錯誤訊息
    else:
        data = stock_data.objects.filter(stock_symbol=stock_symbol)
    result = list(data.values())

    # 計算 KD 指標
    k_values, d_values = calculate_kd(result)

    # 添加 KD 指標到股票數據
    for item, k, d in zip(result[8:], k_values[8:], d_values[8:]):  ## zip()函數用於將可迭代的對象作為參數，將對象中對應的元素打包成一個個元組，然後返回由這些元組組成的列表。
        item['k_value'] = k                               ## 這裡是將k值加入到item中
        item['d_value'] = d                                 
    
    return JsonResponse(result, safe=False)