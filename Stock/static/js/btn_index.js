
BtnRenew = document.querySelector('.btn_renew');
BtnRenew.addEventListener('click', function() {
    BtnRenew.insertAdjacentHTML('beforeend', `
    <div class="spinner-border text-primary spinner-grow-sm m-1" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  `);
    BtnRenew.disabled = true; // 禁用按鈕防止重複點擊
    
 

    fetch(url_+'Stock/renew/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        BtnRenew.textContent = '成功存入資料庫';
        setTimeout(() => {
            BtnRenew.textContent = '更新';
            BtnRenew.disabled = false; // 重新啟用按鈕
        }, 2000); // 2秒後重置按鈕文字
    })
    .catch(error => {
        BtnRenew.textContent = '更新';
        BtnRenew.disabled = false; // 重新啟用按鈕
    });
}); 