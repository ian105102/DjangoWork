# 股票查詢系統
## 基礎介紹
使用python django 框架製作

## 使用方式
### 使用到的python套件:
* asgiref             3.8.1 
* certifi             2024.2.2
* charset-normalizer  3.3.2
* dj-database-url     2.1.0
* Django              4.1
* django-cors-headers 4.3.1
* idna                3.7
* lxml                5.2.1
* pip                 23.3.1
* requests            2.31.0
* setuptools          68.2.2
* sqlparse            0.4.4
* twstock             1.3.1
* typing_extensions   4.11.0
* tzdata              2023.3
* urllib3             2.2.1
* wheel               0.41.2
* whitenoise          6.6.0
### **注意 在檔案base.html 需要url_改成當下的伺服器地址**
```html
    <script>
        const url_ ="https://carefully-unified-duck.ngrok-free.app/"  //改這裡!!!
        const stock_symbol = "{{Data.stock_symbol}}";
    </script>
```
###確認執行完畢後輸入
```
python manage.py runserver
```
