console.log('index.js loaded')
let input = document.querySelector('.input_contnet input');
let Search_box = document.querySelector('.Search_box');
let button = document.querySelector('.submit_btn');
let search = document.querySelector('.search');
let Down_menu = document.querySelector('.Down_menu');

button.addEventListener('click', function() {
    let inputValue = input.value.trim();
    let queue = getQueueFromCookie();

    if (queue.includes(inputValue) || inputValue.length<1) {
        return; 
    }

    if (queue.length >= 4) {
        queue.shift(); 
    }

    // 將新值添加到佇列
    queue.push(inputValue);

    // 更新 Cookie 中的佇列
    document.cookie = `SearchList=${JSON.stringify(queue)}`;
});

function getQueueFromCookie() {
    let queue = [];
    let cookie = document.cookie;

    if (cookie.includes('SearchList=')) {
        let startIndex = cookie.indexOf('SearchList=') + 11;    // 11 是 'SearchList=' 的長度
        let endIndex = cookie.indexOf(';', startIndex);       // 結束索引是分號的索引
        if (endIndex === -1) {
            endIndex = cookie.length;                       // 如果找不到分號，則結束索引是 cookie 的長度
        }
        let queueString = cookie.slice(startIndex, endIndex);   // 從 cookie 中提取佇列的 JSON 字符串
        queue = JSON.parse(queueString);                 // 將 JSON 字符串轉換為陣列
    }       
    return queue;
}
function addQueueToHTML() {
    let queue = getQueueFromCookie();
    queue = queue.reverse(); // 反轉佇列，以便最新的值顯示在最上面
    // 清空 Down_menu 中的內容
    Down_menu.innerHTML = '';

    // 將佇列中的每個值添加到 Down_menu 中
    queue.forEach(function(value) {
        let p = document.createElement('p');
        p.className = 'Search_item';
        p.textContent = value;
        Down_menu.appendChild(p);
        let Search_item = document.querySelector('.Search_item');
    });
    document.querySelectorAll('.Search_item').forEach(function(Search_item) {
        Search_item.addEventListener('click', function(event) {
            input.value = event.target.textContent;
        });
    });
}


input.addEventListener('focus', function(event) {
    Search_box.classList.add('active');
});

input.addEventListener('blur', function(event) {
    Search_box.classList.remove('active');
});

addQueueToHTML();