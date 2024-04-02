
document.addEventListener("DOMContentLoaded", function () {
  // 初始化 Leaflet 地圖   設定出地圖初始 view point   ([經緯度,],縮放比例)
  var map = L.map('map').setView([25.084188, 121.56211], 11);

  // 在地圖上新增 OSM 圖層
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
  }).addTo(map);

  // icon客製化  
  var customIcon = L.icon({
    iconUrl: '../images/soft-drink.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  });


  // 在地圖上新增一個 marker   初始標記
  // var marker = L.marker([25.033, 121.565]).addTo(map);

  // 綁定點擊事件，當使用者點擊地圖時觸發
  map.on('click', function (e) {
      // 取得點擊位置的經緯度
      var latlng = e.latlng;

      // 在地圖上新增一個 marker
      var newMarker = L.marker(latlng, { icon: customIcon }).addTo(map);

      // 綁定 Popup，你可以根據需要自定義內容
      newMarker.bindPopup("<b>使用者新增地標</b><br><b>經緯度</b><br>"+ latlng ).openPopup();

      // 將經緯度資訊送至後端
      sendToBackend(latlng);
  });




  // 傳送經緯度資訊至後端的函數    
  /*
  如何傳送到後端尚未寫，通常使用AJAX 或 Fetch API flask(我們應該會用 傳送成json)
  */
  function sendToBackend(latlng) {
      // 使用 Ajax 或其他方法將經緯度資訊送至後端
      // 僅為示例，實際上需要根據你的後端實作來進行資料傳送
      console.log('Sending to backend:', latlng);
      // 可以使用 Fetch API 或其他 Ajax 方法將資訊傳送到後端  (和刪除一樣尚未研究)
  }
});



/*
 滑動事件失敗 需要隊員協助
*/


// 取得要滑動到的目標元素
var targetElement = document.querySelector('.main');


targetElement.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });

// 創建 Intersection Observer 實例
var observer = new IntersectionObserver(function(entries, observer) {
    // entries 是進入或離開可視區域的元素陣列
    entries.forEach(function(entry) {
        // 如果目標元素進入可視區域
        if (entry.isIntersecting) {
            // 使用 scrollIntoView 方法滑動到目標元素
            targetElement.scrollIntoView({ behavior: 'smooth' });
            
            // 停止觀察，避免重複觸發
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 }); // threshold 代表目標元素與可視區域交叉的比例

// 開始觀察目標元素
observer.observe(targetElement);

