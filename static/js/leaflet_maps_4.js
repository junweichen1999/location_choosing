// leaflet_maps.js
function initMap() {
  let zoom = 17; // 0 - 18
  let center = [25.033, 121.565]; // 中心點座標
  let map = L.map('map').setView(center, zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap', // 商用時必須要有版權出處
    zoomControl: true, // 是否秀出 - + 按鈕
  }).addTo(map);

  // icon客製化
  const customIcon = L.icon({
    iconUrl: '../images/soft-drink.png',
    iconSize: [42, 42],
  });

  // 增加icon 
  const markerCenter = [25.0356037, 121.567275];
  const marker = L.marker(markerCenter, {
    icon: customIcon,
    title: '跟 <a> 的 title 一樣', // 跟 <a> 的 title 一樣
    opacity: 1.0
  }).addTo(map);
}

// 调用初始化函数
initMap();
