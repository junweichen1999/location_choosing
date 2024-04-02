// 當點擊提交按鈕時處理搜索的函數
function search() {
    // 從輸入字段中獲取值
    var address = document.getElementById('searching_Address').value;

    // 使用 AJAX 請求將地址發送到後端 Python 檔案 
    /*
    
    
    
    執行py檔 轉經緯度
    
    
    */
    var xhr = new XMLHttpRequest();
    // POST:把資料傳到後端 /  flask_api   / true:在背景中執行
    xhr.open('POST', '/convert_address', true);  // 將路由改為您 Flask 應用中的 Python 檔案的路由    
    // 宣告主體是json格式  
    xhr.setRequestHeader('Content-Type', 'application/json');

    // 假設後端期望 JSON 數據
    var data = JSON.stringify({ address: address });

    // 當請求完成時的回調函數
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            // 請求成功，處理後端返回的數據
            var responseData = JSON.parse(xhr.responseText);

            // 在這裡可以使用 responseData 處理後端返回的經緯度資料
            var latitude = responseData.latitude;
            var longitude = responseData.longitude;
            
            /*
    
    
    
            把經緯度和地址送到後端
    
    
            */




            // 將瀏覽器位置更改為page2.html，同時將地址、經緯度傳送到後端
            var xhr2 = new XMLHttpRequest();
            xhr2.open('POST', '/process_data', true);  // 修改為您 Flask 應用中的路由
            xhr2.setRequestHeader('Content-Type', 'application/json');

            var data2 = JSON.stringify({ address: address, latitude: latitude, longitude: longitude });

            xhr2.onload = function () {
                // 轉址經緯度如果符合篩選條件 轉址到page2.html 
                if (xhr2.status >= 200 && xhr2.status < 300) {

                     // 將瀏覽器位置更改為page2.html
                    window.location.href = 'page2.html';
                    // 請求成功，處理後端返回的數據
                    
                    /*
                    
                    var responseData2 = JSON.parse(xhr2.responseText);
                    
                    */

                    // 在這裡可以使用 responseData2 處理後端返回的資料
                } else {
                    // 請求失敗，處理錯誤
                    console.error('向後端發送地址時出錯。');
                }
            };

            // 發送第二個請求
            xhr2.send(data2);

        } else {
            // 請求失敗，處理錯誤
            console.error('向後端發送地址轉換請求時出錯。');
        }
    };

    // 發送請求
    xhr.send(data);
}