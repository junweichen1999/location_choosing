function updateTable() {
    var table = document.getElementById("myTable");
    var dropdown = document.getElementById("rowSelector");
    var selectedRows = dropdown.value;

    // 顯示所需行數
    for (var i = 1; i <= table.rows.length; i++) {
        if (i <= selectedRows) {
            table.rows[i - 1].classList.remove("hidden");
        } else {
            table.rows[i - 1].classList.add("hidden");
        }
    }
}

// 初始時隱藏多於的行
window.onload = function () {
    // updateTable();
};