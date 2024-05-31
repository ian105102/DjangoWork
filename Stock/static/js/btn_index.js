
// function getCSRFToken() {
//     const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
//     return decodeURIComponent(cookieValue);
// }

BtnRenew = document.querySelector('.btn_renew');
BtnRenew.addEventListener('click', function() {
    // 將按鈕文字設置為 "等待"
    console.log('按鈕被點擊');
    BtnRenew.innerHTML = '<div class="spinner-border text-primary spinner-grow-sm m-1" role="status">' +
    '<span class="visually-hidden">Loading...</span>' +
  '</div>';
    BtnRenew.disabled = true; // 禁用按鈕防止重複點擊
    
 

    fetch(url_+'Stock/renew/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // 資料成功存入資料庫
        console.log('成功:', data);
        BtnRenew.textContent = '成功存入資料庫';
        setTimeout(() => {
            BtnRenew.textContent = '更新';
            BtnRenew.disabled = false; // 重新啟用按鈕
        }, 2000); // 2秒後重置按鈕文字
    })
    .catch(error => {
        console.error('發生錯誤:', error);
        BtnRenew.textContent = '更新';
        BtnRenew.disabled = false; // 重新啟用按鈕
    });
}); 