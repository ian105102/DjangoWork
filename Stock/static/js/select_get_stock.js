console.log('select_get_stock.js');
console.log(all_month);
let select_len = document.querySelector('.select_len');
let _year_select = document.querySelector('._year_select')
let _month_select = document.querySelector('._month_select')
select_len.addEventListener('change', function() {
    let option = ``;
    let class_name = '';
    if (select_len.value == '1') {
        Object.keys(all_month).forEach(function(key) {
            option += `<option value="${key}">${key}</option>`;
        });
        class_name = 'year_select';
    }else if(select_len.value == '2'){
        Object.keys(all_month).forEach(function(key) {
            option += `<option value="${key}">${key}</option>`;
        });
        class_name = 'month_select';
    }else{
        _year_select.innerHTML = ``;
        _month_select.innerHTML = ``;
        return;
    }
    _month_select.innerHTML = ``;
    let selectHTML = ``;
    if(class_name == 'month_select'){
        selectHTML = `
        <label for="formGroupExampleInput" class="form-label">輸入年份</label>
        <select class="form-select `+class_name+`" aria-label="Default select example">
        <option value="-1">請選擇年份</option>
        ` + option + `
        </select>
        `;
        _year_select.innerHTML = selectHTML;
    }else{
        selectHTML = `
        <label for="formGroupExampleInput" class="form-label">輸入年份</label>
        <div class="input-group">
        <select class="form-select `+class_name+`" aria-label="Default select example">
        <option value="-1">請選擇年份</option>
        ` + option + `
        </select>
        <button class="btn btn-outline-secondary button_year_chart" type="button">顯示圖表</button>
        </div>
        `;
        _year_select.innerHTML = selectHTML;
        document.querySelector('.button_year_chart').addEventListener('click', function() {

            console.log('button_chart');
        });
    }
    
    
    if(class_name == 'year_select'){
        select_year = document.querySelector('.'+class_name);
        select_year.addEventListener('change', function() {
        });
    }else{
        select_month = document.querySelector('.'+class_name);
        select_month.addEventListener('change', function() {
            if(select_month.value == '-1'){
                _month_select.innerHTML = ``;
                return;
            }else{
                let option = ``;
                all_month[select_month.value].forEach(function(key) {
                    option += `<option value="${key}">${key}</option>`;
                });
                let selectHTML = `
                <label for="formGroupExampleInput" class="form-label">輸入月份</label>
                <div class="input-group">
                <select class="form-select `+class_name+`" aria-label="Default select example">
                <option value="-1">請選擇年份</option>
                ` + option + `
                </select>
                <button class="btn btn-outline-secondary button_month_chart" type="button">顯示圖表</button>
                </div>
                `;
                _month_select.innerHTML = selectHTML;
                document.querySelector('.button_month_chart').addEventListener('click', function() {
                    console.log('button_chart');
                });
            }
        });
    }
});
