const gridOptions = {
  columnDefs: [
    // set filters
    { field: 'Tên thuốc', filter: true, aggFunc: 'count',
     cellStyle: params => {
        if (params.node.aggData) {
            return {fontWeight: 'bold', backgroundColor: '#f8f3e8'};
        }
     },
     valueFormatter: params => {
        if (params.node.aggData) {
            return `Tổng: ${params.value} hàng`;
        }
     }},
    { field: 'Hoạt chất', filter: true },
    { field: 'Nhóm Dược lý', filter: true },
    { field: 'Nhóm Hóa dược', filter: true },
    { field: 'Hàm lượng', filter: true },
    { field: 'SĐK', filter: true },
    { field: 'Đường dùng', filter: true },
    { field: 'Dạng bào chế', filter: true },
    { field: 'Quy cách đóng gói', filter: true },
    { field: 'ĐVT', filter: true },
    { field: 'Cơ sở sản xuất', filter: true },
    { field: 'Nước sản xuất', filter: true },
    { field: 'Nhà thầu trúng thầu', filter: true },
    { field: 'Nhóm thầu', filter: true },
    { field: 'Gói mua sắm', filter: true },
    { field: 'Số lượng', valueFormatter: numberFormatter, filter: 'agNumberColumnFilter', aggFunc: 'sum', cellClass: 'ag-right-aligned-cell',
     cellStyle: params => {
        if (params.node.aggData) {
            return {fontWeight: 'bold', backgroundColor: '#f8f3e8'};
        }
     } },
    { field: 'Đơn giá', valueFormatter: numberFormatter, filter: 'agNumberColumnFilter', cellClass: 'ag-right-aligned-cell' },
    { field: 'Thành tiền', valueFormatter: numberFormatter, filter: 'agNumberColumnFilter', aggFunc: 'sum', cellClass: 'ag-right-aligned-cell',
     cellStyle: params => {
        if (params.node.aggData) {
            return {fontWeight: 'bold', backgroundColor: '#f8f3e8'};
        }
     } },
    { field: 'Đợt thầu', filter: true },
    { field: 'Số QĐ', filter: true },
    { field: 'Ngày QĐ', filter: true },
    { field: 'Ngày hết hạn', filter: true },
    { field: 'Tên Bệnh viện', filter: true },
  ],

  defaultColDef: {
    flex: 1,
    minWidth: 200,
    resizable: true,
    floatingFilter: true,
    sortable: true,
  },
  groupIncludeFooter: true,
  groupIncludeTotalFooter: true,
  animateRows: true,
};

function numberFormatter(params) {
    var num = params.value;
    if (num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
}

document.addEventListener("DOMContentLoaded", function() {
    $('.select2').select2({
         width: 'resolve'
    });
    document.getElementById('importButton').addEventListener('click', openDialog);
    document.getElementById('inputFile').addEventListener('change', readFile);
    var data = {'start': ''};
    sendData(data);

    var tabKetQua = document.querySelector('body > div:nth-child(1) > nav > div > ul > li:nth-child(1) > a');
    tabKetQua.addEventListener('click', function () {
        tabOnClick(tabKetQua);
        document.getElementById('ketQuaTrungThau').style.display = 'block';

    })

    var tabDanhMuc = document.querySelector('body > div:nth-child(1) > nav > div > ul > li:nth-child(2) > a');
    tabDanhMuc.addEventListener('click', function () {
        tabOnClick(tabDanhMuc);
        document.getElementById('danhMuc').style.display = 'block';
        chonDanhMuc(1);
        sendData({'dm': ''});
    })

    var tabKetQuaSuDung = document.querySelector('body > div:nth-child(1) > nav > div > ul > li:nth-child(3) > a');
    tabKetQuaSuDung.addEventListener('click', function () {
        tabOnClick(tabKetQuaSuDung);
        document.getElementById('nhapKetQuaSuDung').style.display = 'block';
    })

    var tabTheoDoiCungUng = document.querySelector('body > div:nth-child(1) > nav > div > ul > li:nth-child(4) > a');
    tabTheoDoiCungUng.addEventListener('click', function () {
        tabOnClick(tabTheoDoiCungUng, 'content');
        document.getElementById('theoDoiCungUng').style.display = 'block';
        chonCungUng(1);
    })

    var tabPhanTichABCVEN = document.querySelector('body > div:nth-child(1) > nav > div > ul > li:nth-child(5) > a');
    tabPhanTichABCVEN.addEventListener('click', function () {
        tabOnClick(tabPhanTichABCVEN, 'content');
        document.getElementById('phanTichABCVEN').style.display = 'block';
    })

    var gridDiv = document.querySelector('#exampleGrid');
    new agGrid.Grid(gridDiv, gridOptions);
    var gridDivTheoThang = document.querySelector('#gridDivTheoThang');
    new agGrid.Grid(gridDivTheoThang, gridTheoThang);
    var gridDivTongHop = document.querySelector('#gridTongHop');
    new agGrid.Grid(gridDivTongHop, gridTongHop);
    var gridDivCanhBao = document.querySelector('#gridCanhBao');
    new agGrid.Grid(gridDivCanhBao, gridCanhBao);
    var gridDivTonLe = document.querySelector('#gridTonLe');
    new agGrid.Grid(gridDivTonLe, gridTonLe);
})

// Tab Nhập KQTT
function changeNavCon(nav) {
    var activeNav = document.querySelector('#navKetQuaTrungThau > li > a.active');
    activeNav.classList.remove('active');
    activeNav.removeAttribute('aria-current');

    nav.classList.add('active');
    nav.setAttribute('aria-current', 'page');

    var contents = document.querySelectorAll('.navCon');
    for (let c of contents) {
        c.style.display = 'none';
    }
}

// Nhập KQTT > Đợt thầu
function divDotThau() {
    var navDotThau = document.querySelector('#navKetQuaTrungThau > li:nth-child(1) > a');
    changeNavCon(navDotThau);
    document.getElementById('nhapDotThau').style.display = 'block';
}

function divKQTT() {
    var navKQTT = document.querySelector('#navKetQuaTrungThau > li:nth-child(2) > a');
    changeNavCon(navKQTT);
    document.getElementById('nhapKetQuaTrungThau').style.display = 'block';
    var data = {'start': ''};
    sendData(data);
}

function divBaoCaoTongHop() {
    var navBCTH = document.querySelector('#navKetQuaTrungThau > li:nth-child(3) > a');
    changeNavCon(navBCTH);
    document.getElementById('baoCaoTongHop').style.display = 'block';
}

function hienBaoCaoTongHop(ketQuaList) {
    gridOptions.api.setRowData(ketQuaList);
}

function xuatExcellBCTT() {
    gridOptions.api.exportDataAsExcel();
}

var maDotThauList = [];
function btnThemDotThau() {
    var maDotThau = document.getElementById('maDotThau').value;
    var tenDotThau = document.getElementById('tenDotThau').value;
    var giaiDoan = document.getElementById('giaiDoan').value;
    var hinhThucDauThau = document.getElementById('hinhThucDauThau').value;
    var goiMuaSam = document.getElementById('goiMuaSam').value;
    var soQD = document.getElementById('soQD').value;
    var ngayQD = document.getElementById('ngayQD').value;
    var ngayHetHan = document.getElementById('ngayHetHan').value;
    var tenBenhVien = document.getElementById('tenBenhVien').value;
    var ghiChu = document.getElementById('ghiChu').value;

    var dataDotThau = [maDotThau, tenDotThau, giaiDoan, hinhThucDauThau, goiMuaSam, soQD, ngayQD, ngayHetHan, tenBenhVien, ghiChu];
    if (maDotThauList.includes(maDotThau)) {
        alert('Mã đợt thầu đã tồn tại. Vui lòng điền mã khác.');
    } else {
        sendData({'dataDotThau': dataDotThau});
    }
}

function btnCapNhatDotThau() {
    var idDotThau = parseInt(document.querySelector('#bodyDotThau > tr.table-primary').cells[11].innerText);
    var maDotThau = document.getElementById('maDotThau').value;
    var tenDotThau = document.getElementById('tenDotThau').value;
    var giaiDoan = document.getElementById('giaiDoan').value;
    var hinhThucDauThau = document.getElementById('hinhThucDauThau').value;
    var goiMuaSam = document.getElementById('goiMuaSam').value;
    var soQD = document.getElementById('soQD').value;
    var ngayQD = document.getElementById('ngayQD').value;
    var ngayHetHan = document.getElementById('ngayHetHan').value;
    var tenBenhVien = document.getElementById('tenBenhVien').value;
    var ghiChu = document.getElementById('ghiChu').value;

    var dataDotThau = [maDotThau, tenDotThau, giaiDoan, hinhThucDauThau, goiMuaSam, soQD, ngayQD, ngayHetHan, tenBenhVien, ghiChu];
    var data = {'dataUpdateDotThau': {
        "type": "update",
        "idDotThau": idDotThau,
        "data": dataDotThau,
    }};
    sendData(data);
}

function btnXoaDotThau() {
    var idDotThau = parseInt(document.querySelector('#bodyDotThau > tr.table-primary').cells[11].innerText);
    var maDotThau = document.querySelector('#bodyDotThau > tr.table-primary').cells[1].innerText;
    var data = {'dataUpdateDotThau': {
        "type": "delete",
        "idDotThau": idDotThau,
    }};
    var index = maDotThauList.indexOf(maDotThau);
    if (index !== -1) {
        maDotThauList.splice(index, 1);
    }
    sendData(data);
}

function formatDate(datetime) {
    var date = new Date(datetime);
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');

    var formattedDateStr = `${year}-${month}-${day}`;

    return formattedDateStr;
}

function hienThiDanhMucDotThau(danhmuc) {
    var html = '';
    var i = 1;
    for (let row of danhmuc) {
        html += `
            <tr>
                <th>${i}</th>
                <td>${row[1]}</td>
                <td>${row[2]}</td>
                <td>${row[3]}</td>
                <td>${row[4]}</td>
                <td>${row[5]}</td>
                <td>${row[6]}</td>
                <td>${formatDate(row[7])}</td>
                <td>${formatDate(row[8])}</td>
                <td>${row[9]}</td>
                <td>${row[10]}</td>
                <td style="display: none">${row[0]}</td>
            </tr>
        `;
        i++;
    }
    document.getElementById('bodyDotThau').innerHTML = html;
    selectedRowTableDotThau();
}

function hienDataListBenhVien(danhmuc) {
    var dataListBenhVien = [];
    for (let row of danhmuc) {
        if (!dataListBenhVien.includes(row[9])) {
            dataListBenhVien.push(row[9]);
        }

        maDotThauList.push(row[1]);
    }

    var html = '';
    for (let bv of dataListBenhVien) {
        html += `<option value="${bv}"></option>`;
    }
    document.getElementById('datalistBenhVien').innerHTML = html;

    var html = '';
    for (let mdt of maDotThauList) {
        html += `<option value="${mdt}"></option>`;
    }
    document.getElementById('datalistMaDotThau').innerHTML = html;
}

function selectedRowTableDotThau() {
    var tableRows = document.querySelectorAll('#bodyDotThau > tr');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            if (!this.classList.contains('table-primary')) {
                var selectedRow = document.querySelector('tr.table-primary');
                if (selectedRow) {
                    selectedRow.classList.remove('table-primary');
                }

                this.classList.add('table-primary');
                hienInputDotThau(this);
            } else {
                this.classList.remove('table-primary');
            }
        });
    });
}

function hienInputDotThau(tr) {
    var cells = tr.cells;
    document.getElementById('maDotThau').value = cells[1].innerText;
    document.getElementById('tenDotThau').value = cells[2].innerText;
    document.getElementById('giaiDoan').value = cells[3].innerText;
    document.getElementById('hinhThucDauThau').value = cells[4].innerText;
    document.getElementById('goiMuaSam').value = cells[5].innerText;
    document.getElementById('soQD').value = cells[6].innerText;
    document.getElementById('ngayQD').value = cells[7].innerText;
    document.getElementById('ngayHetHan').value = cells[8].innerText;
    document.getElementById('tenBenhVien').value = cells[9].innerText;
    document.getElementById('ghiChu').value = cells[10].innerText;
}

// Nhập KQTT > KQTT
function selectThongTinChung(list, id) {
    var html = '<option></option>';
    for (let item of list) {
        html += `<option>${item}</option>`;
    }
    document.getElementById(id).innerHTML = html;
}

function changeSlMaDotThau() {
    var maDotThau = document.getElementById('slMaDotThau').value;
    if (maDotThau !== '') {
        sendData({'chonMaDotThau': maDotThau});
    }
}

function hienThiDotThauTheoMaDotThau(thongtin) {
    document.getElementById('slDotThau').value = thongtin[2];
    document.getElementById('slGiaiDoan').value = thongtin[3];
    document.getElementById('slHinhThucDauThau').value = thongtin[4];
    document.getElementById('slGoiMuaSam').value = thongtin[5];
    document.getElementById('slSoQD').value = thongtin[6];
    document.getElementById('slNgayQD').value = formatDate(thongtin[7]);
    document.getElementById('slNgayHetHan').value = formatDate(thongtin[8]);
    document.getElementById('slTenBenhVien').value = thongtin[9];
}

function hienLichSuImport(lichSuImport) {
    var html = '';
    var i = 1;
    for (let row of lichSuImport) {
        html += `
            <tr>
                <th>${i}</th>
                <td>${row[1]}</td>
                <td>${row[2]}</td>
                <td style="display: none">${row[0]}</td>
            </tr>
        `;
        i++;
    }
    document.getElementById('tableLichSu').innerHTML = html;
    selectedRowTableLichSu();
}

function openDialog() {
    document.getElementById('inputFile').click();
}

var dataExcel = [];
var columnNames = ['TT', 'Tên thuốc', 'Hoạt chất', 'Hàm lượng', 'SĐK', 'Đường dùng', 'Dạng bào chế',
'Cơ sở sản xuất', 'Nước sản xuất', 'Quy cách đóng gói', 'Nhà thầu trúng thầu', 'ĐVT', 'Số lượng', 'Đơn giá', 'Thành tiền', 'Nhóm thầu'];
function readFile() {
    var file = document.getElementById('inputFile').files[0];
    if (file) {
      const reader = new FileReader();

      reader.onload = function (e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });

        const firstSheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[firstSheetName];
        const excelData = XLSX.utils.sheet_to_json(sheet);

        var columnFile = Object.keys(excelData[0]);
        var check = compareList(columnNames, columnFile);
        if (check) {
            document.getElementById('tableChiTietThuoc').innerHTML = hienThiDuLieu(excelData);
            dataExcel = JSON.parse(JSON.stringify(excelData));
        } else {
            alert('Vui lòng import file có chứa các cột như file mẫu.');
        }
      };

      reader.readAsArrayBuffer(file);
    }
}

function hienThiDuLieu(excelData) {
    var html = '';
    let i = 1;
    for (let row of excelData) {
        html += `<tr>
            <th>${i}</th>
            <td contenteditable="true">${row['Tên thuốc']}</td>
            <td contenteditable="true">${row['Hoạt chất']}</td>
            <td contenteditable="true">${row['Hàm lượng']}</td>
            <td contenteditable="true">${row['SĐK']}</td>
            <td contenteditable="true">${row['Đường dùng']}</td>
            <td contenteditable="true">${row['Dạng bào chế']}</td>
            <td contenteditable="true">${row['Quy cách đóng gói']}</td>
            <td contenteditable="true">${row['ĐVT']}</td>
            <td contenteditable="true">${row['Cơ sở sản xuất']}</td>
            <td contenteditable="true">${row['Nước sản xuất']}</td>
            <td contenteditable="true">${row['Nhà thầu trúng thầu']}</td>
            <td contenteditable="true">${row['Nhóm thầu']}</td>
            <td contenteditable="true">${row['Số lượng'].toLocaleString()}</td>
            <td contenteditable="true">${row['Đơn giá'].toLocaleString()}</td>
            <td contenteditable="true">${row['Thành tiền'].toLocaleString()}</td>
            </tr>`;
        i++;
    }
    return html;
}

function huyImport() {
    document.getElementById('inputFile').value = '';
}

function compareList(list1, list2) {
    if (list1.length != list2.length) {
        return false;
    }
    for (let item of list1) {
        if (!list2.includes(item)) {
            return false;
        }
    }
    return true;
}

function luuChiTietThuoc() {
    var maDotThau = document.getElementById('slMaDotThau').value;
    var dataChiTietThuoc = [];
    var rowsChiTietThuoc = document.getElementById('tableChiTietThuoc').rows;

    for (let row of rowsChiTietThuoc) {
        var rowData = [];
        for (let cell of row.cells) {
            rowData.push(cell.textContent);
        }
        dataChiTietThuoc.push(rowData);
    }
    var data = {
        'maDotThau': maDotThau,
        'data': dataChiTietThuoc
    };
    if (maDotThau === "") {
        alert('Vui lòng chọn mã đợt thầu.');
    } else {
        sendData({'luuChiTietThuoc': data});
        huyImport();
        document.getElementById('tableChiTietThuoc').innerHTML = '';
    }
}

function xoaDuLieuImport() {
    var selectedRow = document.querySelector('#tableLichSu > tr.table-primary');
    var idLichSu = parseInt(selectedRow.cells[3].innerText);
    sendData({'xoaDuLieuImport': idLichSu});
}

function selectedRowTableLichSu() {
    var tableRows = document.querySelectorAll('#tableLichSu > tr');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            if (!this.classList.contains('table-primary')) {
                var selectedRow = document.querySelector('tr.table-primary');
                if (selectedRow) {
                    selectedRow.classList.remove('table-primary');
                }
                this.classList.add('table-primary');
            } else {
                this.classList.remove('table-primary');
            }
        });
    });
}

// Menu chung
function tabOnClick(tab) {
    var activeTab = document.querySelector('.active');
    activeTab.classList.remove('active');
    activeTab.removeAttribute('aria-current');

    tab.classList.add('active');
    tab.setAttribute('aria-current', 'page');

    var contents = document.querySelectorAll('.content');
    for (let c of contents) {
        c.style.display = 'none';
    }
}

// Danh mục
function chonDanhMuc(i) {
    var anchor = document.querySelector(`#navDanhMuc > li:nth-child(${i}) > a`);
    var activeNav = document.querySelector('#navDanhMuc > li > a.active');
    if (activeNav) {
        activeNav.classList.remove('active');
        activeNav.removeAttribute('aria-current');
    }
    anchor.classList.add('active');
    anchor.setAttribute('aria-current', 'page');
    var divDanhMuc = document.querySelectorAll('div.danhMuc');
    divDanhMuc.forEach(function(div) {
        div.style.display = 'none';
    });
    var targetDiv = divDanhMuc[i-1];
    if (targetDiv) {
        targetDiv.style.display = 'block';
    }
    selectedRows = [];
}


function hienThiDanhMuc(danhMucDict) {
    var anchors = document.querySelectorAll('#navDanhMuc > li > a');
    var tableDanhMucs = document.querySelectorAll('div.danhMuc > table > tbody');
    for (let i = 0; i < anchors.length; i++) {
        var dm = anchors[i].getAttribute('name');
        var danhmuc = danhMucDict[dm];
        var html = '';
        var k = 1;
        if (danhmuc.length > 0) {
            if (dm === 'danhmuchoatchatbenhvien') {
                for (let row of danhmuc) {
                    if (row[1] === null) {
                        row[1] = '';
                    }
                    if (row[2] === null) {
                        row[2] = '';
                    }
                    html += `
                        <tr>
                            <th>${k}</th>
                            <td>${row[1]}</td>
                            <td>${row[2]}</td>
                            <td>${row[3]}</td>
                            <td>${row[4]}</td>
                            <td>${row[5]}</td>
                            <td style="display: none">${row[0]}</td>
                        </tr>
                    `;
                    k++;
                }
            } else {
                for (let row of danhmuc) {
                    html += `<tr>
                        <th>${k}</th>
                        <td>${row[1]}</td>
                        <td style="display: none">${row[0]}</td>
                    <tr>`
                    k++;
                }
            }
        tableDanhMucs[i].innerHTML = html;
        chonHang(i);
        }
    }
}

var selectedRows = [];

function chonHang(i) {
    selectedRows = [];
    var tableRows = document.querySelectorAll(`#danhMuc > div > div.col-10 > div:nth-child(${i}) > table > tbody > tr`);
    tableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            if (!selectedRows.includes(this)) {
                selectedRows.push(this);
                this.classList.add('table-primary');
            } else {
                selectedRows = selectedRows.filter(item => item !== this);
                this.classList.remove('table-primary');
            }
        });

        var cells = Array.from(row.cells);
        cells.forEach(function(cell) {
            cell.addEventListener('dblclick', function() {
                cell.setAttribute('contenteditable', 'true');
            });
        });
    });
}



function gopGiaTri() {
    var dm = document.querySelector('#navDanhMuc > li > a.active').getAttribute('name');
    var rowIdList = [];
    var gopHoatChat = {};
    if (dm !== 'danhmuchoatchatbenhvien') {
        for (row of selectedRows) {
            var cells = row.cells;
            var rowID = parseInt(cells[cells.length - 1].innerText);
            rowIdList.push(rowID);
        }
    } else {
        for (row of selectedRows) {
            var cells = row.cells;
            var rowID = parseInt(cells[cells.length - 1].innerText);
            rowIdList.push(rowID);
            var maHoatChat = cells[1].innerText;
            var sttTT20 = cells[2].innerText;
            if (maHoatChat !== '') {
                gopHoatChat['maHoatChat'] = maHoatChat;
            }
            if (sttTT20 !== '') {
                gopHoatChat['sttTT20'] = sttTT20;
                gopHoatChat['idRowSTTTT20'] = rowID;
            }
        }
    }
    var data = {
        'danhmuc': dm,
        'rowIdList': rowIdList,
        'gopHoatChat': gopHoatChat
    }
    sendData({'gopDuLieu': data});
}

// Theo dõi cung ứng thuốc
function chonThuMucKhoChan() {
    var input = document.getElementById('directoryKhoChan');
    input.click();
    input.addEventListener('change', (event) => {
        let output = document.getElementById("listingKhoChan");
        output.innerHTML = '';
        var files = event.target.files;
        fileKho(files, output);
        input.value = '';
    })
}

function chonThuMucKhoLe() {
    var input = document.getElementById('directoryKhoLe');
    input.click();
    input.addEventListener('change', (event) => {
        let output = document.getElementById("listingKhoLe");
        output.innerHTML = '';
        var files = event.target.files;
        fileKho(files, output);
        input.value = '';
    });
}

function fileKho(files, output) {
    var formData = new FormData();
    for (const file of files) {
        let item = document.createElement("li");
        item.textContent = file.webkitRelativePath;
        output.appendChild(item);
        formData.append('files', file);
        formData.append('date', file.lastModifiedDate);
    }
    $.ajax({
        url: '/files',
        type: 'POST',
        data: formData,
        success: function (response) {
        },
        cache: false,
        contentType: false,
        processData: false
    });
}

function theodoicungung() {
    sendData({'cungUng': ''});
}

// Theo dõi cung ứng
function chonCungUng(i) {
    var anchor = document.querySelector(`#navCungUng > li:nth-child(${i}) > a`);
    var activeNav = document.querySelector('#navCungUng > li > a.active');
    if (activeNav) {
        activeNav.classList.remove('active');
        activeNav.removeAttribute('aria-current');
    }
    anchor.classList.add('active');
    anchor.setAttribute('aria-current', 'page');
    var divCungUng = document.querySelectorAll('div.cungUng');
    divCungUng.forEach(function(div) {
        div.style.display = 'none';
    });
    var targetDiv = divCungUng[i-1];
    if (targetDiv) {
        targetDiv.style.display = 'block';
    }
}

const gridCanhBao = {
  columnDefs: [
    { headerName: 'Ngày trúng thầu', field: 'ngayTrungThau', filter: true },
    { headerName: 'Thuốc', field: 'tenThuoc', filter: true },
    { headerName: 'Hoạt chất', field: 'hoatChat', filter: true },
    { headerName: 'Nhóm thầu', field: 'nhomThau', filter: true },
    { headerName: 'Nhóm Dược lý', field: 'nhomDuocLy', filter: true },
    { headerName: 'Nhóm Hóa dược', field: 'nhomHoaDuoc', filter: true },
    { headerName: 'Tổng kế hoạch', field: 'tongKeHoach', filter: 'agNumberColumnFilter' },
    { headerName: 'Đã sử dụng', field: 'daSuDung', filter: 'agNumberColumnFilter' },
    { headerName: '%Sử dụng', field: 'phanTramSuDung', filter: true },
    { headerName: 'Còn lại', field: 'conLai', filter: 'agNumberColumnFilter' },
    { headerName: '%Còn lại', field: 'phanTramConLai', filter: true },
  ],
  defaultColDef: {
    flex: 1,
    minWidth: 100,
    resizable: true,
    floatingFilter: true,
    sortable: true,
  },
  animateRows: true,
};



const gridTheoThang = {
  columnDefs: [
    { headerName: 'Tên thuốc', field: 'tenThuoc', filter: true, minWidth: 300, cellClass: 'ag-left-aligned-cell' },
    { headerName: 'Hoạt chất', field: 'hoatChat', filter: true, minWidth: 300, cellClass: 'ag-left-aligned-cell' },
    { headerName: 'Kế hoạch', field: 'keHoach', minWidth: 150, valueFormatter: numberFormatter },
    { headerName: 'Tổng sử dụng', field: 'tongSuDung', valueFormatter: numberFormatter, minWidth: 150 },
    { headerName: 'Còn lại', field: 'conLai', valueFormatter: numberFormatter, minWidth: 150 },
    { headerName: '%Còn lại', field: 'phanTramConLai', valueFormatter: numberFormatter, minWidth: 150 },
    { headerName: 'T3', field: '03', valueFormatter: numberFormatter },
    { headerName: 'T4', field: '04', valueFormatter: numberFormatter },
    { headerName: 'T5', field: '05', valueFormatter: numberFormatter },
    { headerName: 'T6', field: '06', valueFormatter: numberFormatter },
    { headerName: 'T7', field: '07', valueFormatter: numberFormatter },
    { headerName: 'T8', field: '08', valueFormatter: numberFormatter },
    { headerName: 'T9', field: '09', valueFormatter: numberFormatter },
    { headerName: 'T10', field: '10', valueFormatter: numberFormatter },
    { headerName: 'T11', field: '11', valueFormatter: numberFormatter },
    { headerName: 'T12', field: '12', valueFormatter: numberFormatter },
    { headerName: 'T1', field: '01', valueFormatter: numberFormatter },
    { headerName: 'T2', field: '02', valueFormatter: numberFormatter },
  ],
  defaultColDef: {
    flex: 1,
    minWidth: 100,
    resizable: true,
    floatingFilter: true,
    sortable: true,
    filter: 'agNumberColumnFilter', cellClass: 'ag-right-aligned-cell',
     cellStyle: params => {
        if (params.node.aggData) {
            return {fontWeight: 'bold', backgroundColor: '#f8f3e8'};
        }
     }
  },
  animateRows: true,
};

function updateSuDungTheoThang(ketQuaCungUng) {
    const startYear = '2022';
    const endYear = '2023';

    var danhsachthaulist = ketQuaCungUng['danhsachthaulist'];
    var suDungTheoThang = ketQuaCungUng['suDungTheoThang'];
    var danhsachthuoc = ketQuaCungUng['danhsachthuoc'];
    var months = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '01', '02'];

   $('#limitMonth').on('change', function() {
        gridTheoThang.columnApi.setColumnsVisible(months, true);
        if (document.getElementById('checkSuDung').checked) {
            var monthNum = parseInt(this.value);
            updateLimitThang(ketQuaCungUng, monthNum);
        }
   })

   $('#checkSuDung').on('change', function() {
        var checkSuDung = this.checked;
        if (checkSuDung) {
            var monthNum = parseInt(document.getElementById('limitMonth').value);
            updateLimitThang(ketQuaCungUng, monthNum);

        } else {
            gridTheoThang.columnApi.setColumnsVisible(months, true);
            updateSuDungTheoThang(ketQuaCungUng);
        }
   })

    var rowData = [];
    for (var thuoc of danhsachthuoc) {
        var rowThuoc = {
            'tenThuoc': thuoc[0],
            'hoatChat': thuoc[1],
            'keHoach': thuoc[2],
            '01': 0,
            '02': 0,
            '03': 0,
            '04': 0,
            '05': 0,
            '06': 0,
            '07': 0,
            '08': 0,
            '09': 0,
            '10': 0,
            '11': 0,
            '12': 0,
        };
        var sum = 0;
        for (var row of suDungTheoThang) {
            if (row[1] == thuoc[0]) {
                var month = row[0].split('-')[1];
                if (row[0].startsWith(startYear)) {
                    if (!['01', '02'].includes(month)) {
                        rowThuoc[month] = parseInt(row[2]);
                        sum += parseInt(row[2]);
                    }
                } else if (row[0].startsWith(endYear)) {
                    if (['01', '02'].includes(month)) {
                        rowThuoc[month] = parseInt(row[2]);
                        sum += parseInt(row[2]);
                    }
                }
            }
        }
        rowThuoc['tongSuDung'] = sum;
        rowThuoc['conLai'] = thuoc[2] - sum;
        rowThuoc['phanTramConLai'] = `${(rowThuoc['conLai']*100/thuoc[2]).toFixed(2)}%`;
        rowData.push(rowThuoc);
    }
    gridTheoThang.api.setRowData(rowData);
}

function updateLimitThang(ketQuaCungUng, monthNum) {
    var suDungTheoThang = ketQuaCungUng['suDungTheoThang'];
    var danhsachthuoc = ketQuaCungUng['danhsachthuoc'];

    var startYear = '2022';
    var endYear = '2023';

    var rowData = [];
    for (var thuoc of danhsachthuoc) {
        var rowThuoc = {
            'tenThuoc': thuoc[0],
            'hoatChat': thuoc[1],
            'keHoach': thuoc[2],
            '01': 0,
            '02': 0,
            '03': 0,
            '04': 0,
            '05': 0,
            '06': 0,
            '07': 0,
            '08': 0,
            '09': 0,
            '10': 0,
            '11': 0,
            '12': 0,
        };
        var months = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '01', '02'];
        var sum = 0;
        var i = 0;
        for (var row of suDungTheoThang) {
            if (row[1] == thuoc[0]) {
                var month = row[0].split('-')[1];
                if (row[0].startsWith(startYear)) {
                    if (!['01', '02'].includes(month)) {
                        if (months.indexOf(month) < monthNum) {
                            rowThuoc[month] = parseInt(row[2]);
                            sum += parseInt(row[2]);
                        }
                    }
                } else if (row[0].startsWith(endYear)) {
                    if (['01', '02'].includes(month)) {
                        if (months.indexOf(month) < monthNum) {
                            rowThuoc[month] = parseInt(row[2]);
                            sum += parseInt(row[2]);
                        }
                    }
                }
            }
        }
        rowThuoc['tongSuDung'] = sum;
        if (sum >= thuoc[2]) {
            rowData.push(rowThuoc);
        }
        for (i = 0; i < months.length; i++) {
            if (i >= monthNum) {
                gridTheoThang.columnApi.setColumnVisible(months[i], false);
            }
        }
        rowThuoc['conLai'] = thuoc[2] - sum;
        rowThuoc['phanTramConLai'] = `${(rowThuoc['conLai']*100/thuoc[2]).toFixed(2)}%`;
    }
    gridTheoThang.api.setRowData(rowData);
}


function hienThiKetQuaCungUng(ketQuaCungUng) {
    updateSuDungTheoThang(ketQuaCungUng);
    var slThuoc = document.getElementById('selectThuocCungUng');
    var slHoatChat = document.getElementById('selectHoatChatCungUng');
    var slNhomDuocLy = document.getElementById('selectNhomDuocLyCungUng');
    var slNhomHoaDuoc = document.getElementById('selectNhomHoaDuocCungUng');

    var danhsachthau = ketQuaCungUng['danhsachthau'];
    slThuoc.innerHTML = setOptions(9, danhsachthau);
    slHoatChat.innerHTML = setOptions(10, danhsachthau);
    slNhomDuocLy.innerHTML = setOptions(11, danhsachthau);
    slNhomHoaDuoc.innerHTML = setOptions(12, danhsachthau);

    var htmlConLai = '';
    var htmlSuDung = '';
    var htmlTonLe = '';
    var htmlTonLeLon = '';
    var htmlTongHop = '';
    for (let row of danhsachthau) {
        if (row[2]/row[1] <= 0.1) {
            htmlSuDung += conLaivaSuDung(row);
        }
        if (row[3]/row[1] <= 0.1) {
            htmlConLai += conLaivaSuDung(row);
        }
        if (row[5]/row[4] <= 0.1) {
            htmlTonLe += tonLe(row);
        }
        if (row[5]/row[4] > 0.1) {
            htmlTonLeLon += tonLe(row);
        }
    }
    document.getElementById('tableConLai').innerHTML = htmlConLai;
    document.getElementById('tableSuDung').innerHTML = htmlSuDung;
    document.getElementById('tableTonLe').innerHTML = htmlTonLe;
    document.getElementById('tableTonLeLon').innerHTML = htmlTonLeLon;

    sortTable(document.getElementById('tableNhomThau').parentElement);
    sortTable(document.getElementById('tableDuocLy').parentElement);
    sortTable(document.getElementById('tableHoaDuoc').parentElement);
    sortTable(document.getElementById('tableConLai').parentElement);
    sortTable(document.getElementById('tableSuDung').parentElement);
    sortTable(document.getElementById('tableTonLe').parentElement);
    sortTable(document.getElementById('tableTonLeLon').parentElement);

    var thongkekho = ketQuaCungUng['thongkekho'];
    $('#selectThuocCungUng').on('change', function () {
        var idThuoc = this.value;

        var selectedRow = danhsachthau.find(row => row[8] == idThuoc);
        if (selectedRow) {
            document.getElementById('tongKeHoach').innerHTML = selectedRow[1].toLocaleString();
            var daSuDungPercentage = (selectedRow[2] * 100 / selectedRow[1]).toFixed(2);
            document.getElementById('daSuDung').innerHTML = `${selectedRow[2].toLocaleString()} (${daSuDungPercentage}%)`;
            document.getElementById('soLanDuTru').innerHTML = selectedRow[7].toLocaleString();
        }

        var html = '';
        for (let row of thongkekho) {
            if (row[2] == idThuoc) {
                html += `<tr>
                    <td>${formatDate(row[1])}</td>
                    <td>${row[3].toLocaleString()}</td>
                    <td>${row[4].toLocaleString()}</td>
                    <td>${row[5].toLocaleString()}</td>
                    <td>${row[6].toLocaleString()}</td>
                </tr>`;
            }
        }
        document.getElementById('tableThuoc').innerHTML = html;
    })

    $('#selectHoatChatCungUng').on('change', function () {
        var hoatChat = this.value;
        document.getElementById('tableNhomThau').innerHTML = cungUngTheoNhom(10, hoatChat, danhsachthau);
    })

    $('#selectNhomDuocLyCungUng').on('change', function () {
        var nhomDuocLy = this.value;
        document.getElementById('tableDuocLy').innerHTML = cungUngTheoNhom(11, nhomDuocLy, danhsachthau);
    })

    $('#selectNhomHoaDuocCungUng').on('change', function () {
        var nhomHoaDuoc = this.value;
        document.getElementById('tableHoaDuoc').innerHTML = cungUngTheoNhom(12, nhomHoaDuoc, danhsachthau);
    })
}

function setOptions(index, danhsachthau) {
    var list = [];
    var html = '<option value="">Chọn</option>';

    for (let row of danhsachthau) {
        if (!list.includes(row[index])) {
            list.push(row[index]);
            if (index == 9) {
                html += `<option value="${row[8]}">${row[index]}</option>`;
            } else {
                html += `<option value="${row[index]}">${row[index]}</option>`;
            }
        }
    }
    return html;
}

function cungUngTheoNhom(index, value, danhsachthau) {
    var html = '';
    for (let row of danhsachthau) {
        if (row[index] == value) {
            html += `<tr>
                <td>${formatDate(row[0])}</td>
                <td>${row[13]}</td>
                <td>${row[9]}</td>
                <td>${row[10]}</td>
                <td>${row[1].toLocaleString()}</td>
                <td>${row[2].toLocaleString()}</td>
                <td class="specialCol">${(100*row[2]/row[1]).toFixed(2)}%</td>
                <td>${row[3].toLocaleString()}</td>
                <td class="specialCol">${(100*row[3]/row[1]).toFixed(2)}%</td>
                <td>${row[6].toLocaleString()}</td>
                <td>${row[7]}</td>
            </tr>`;
        }
    }
    return html;
}

function conLaivaSuDung(row, i) {
    var html = `<tr>
        <td>${formatDate(row[0])}</td>
        <td>${row[9]}</td>
        <td>${row[10]}</td>
        <td>${row[13]}</td>
        <td>${row[11]}</td>
        <td>${row[12]}</td>
        <td>${row[1].toLocaleString()}</td>
        <td>${row[2].toLocaleString()}</td>
        <td class="specialCol">${(100*row[2]/row[1]).toFixed(2)}%</td>
        <td>${row[3].toLocaleString()}</td>
        <td class="specialCol">${(100*row[3]/row[1]).toFixed(2)}%</td>
    </tr>`;
    return html;
}

function tonLe(row) {
    var html = `<tr>
                <td>${formatDate(row[0])}</td>
                <td>${row[9]}</td>
                <td>${row[10]}</td>
                <td>${row[13]}</td>
                <td>${row[11]}</td>
                <td>${row[12]}</td>
                <td>${row[5].toLocaleString()}</td>
                <td>${row[4].toLocaleString()}</td>
                <td class="specialCol">${(100*row[5]/row[4]).toFixed(2)}%</td>
            </tr>`;
    return html;
}

function sortTable(table) {
    var headers = table.rows[0].cells;
    console.log(headers);
    for (let i = 0; i < headers.length; i++) {
        headers[i].addEventListener('click', function() {
            console.log('he');
            var switching = true;
            var dir = "asc";
            var switchCount = 0;
            while (switching) {
                switching = false;
                var rows = table.rows;
                for (var r = 1; r < (rows.length - 1); r++) {
                    var shouldSwitch = false;
                    var x = rows[r].cells[i].textContent;
                    var y = rows[r + 1].cells[i].textContent;

                    // Kiểm tra nếu x và y có thể được chuyển đổi thành số
                    var xNum = parseFloat(x.replace(/%|,/g, ''));
                    var yNum = parseFloat(y.replace(/%|,/g, ''));

                    // So sánh xNum và yNum nếu chúng là số, ngược lại, so sánh chuỗi
                    if (!isNaN(xNum) && !isNaN(yNum)) {
                        if (dir == "asc") {
                            if (xNum > yNum) {
                                shouldSwitch = true;
                                break;
                            }
                        } else if (dir == "desc") {
                            if (xNum < yNum) {
                                shouldSwitch = true;
                                break;
                            }
                        }
                    } else {
                        if (dir == "asc") {
                            if (x.toLowerCase() > y.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                            }
                        } else if (dir == "desc") {
                            if (x.toLowerCase() < y.toLowerCase()) {
                                shouldSwitch = true;
                                break;
                            }
                        }
                    }
                }
                if (shouldSwitch) {
                    rows[r].parentNode.insertBefore(rows[r + 1], rows[r]);
                    switching = true;
                    switchCount++;
                } else {
                    if (switchCount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        })
    }
}

function xuatExcell(button) {
    var parentDiv = button.parentElement;
    var divs = parentDiv.children;
    for (div of divs) {
        if (div.style['display'] == 'block') {
            console.log(div);
        }
    }
}


// Phân tích ABC/VEN
function chonFileACB() {
    var input = document.getElementById('inputFileABC');
    input.click();
    input.addEventListener('change', (event) => {
        var file = event.target.files[0];
        document.getElementById('fileNameInput').value = file.name;
        var formData = new FormData;
        formData.append('file', file);
        $.ajax({
            url: '/files',
            type: 'POST',
            data: formData,
            success: function (response) {
            },
            cache: false,
            contentType: false,
            processData: false
        });
        input.value = '';
    });
}

function sendData(data) {
    $.ajax({
        url: '/',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(response) {
            console.log(response);
            if (response.ketQuaList) {
//                hienSelectKQTT(response.ketQuaList);
                hienBaoCaoTongHop(response.ketQuaList);
            }

            if (response.danhMucDict) {
                hienThiDanhMuc(response.danhMucDict);
            }

            if (response.danhMucDotThau) {
                hienThiDanhMucDotThau(response.danhMucDotThau);
                hienDataListBenhVien(response.danhMucDotThau);
            }

            if (response.maDotThau) {
                selectThongTinChung(response.maDotThau, 'slMaDotThau');
            }

            if (response.thongTin) {
                hienThiDotThauTheoMaDotThau(response.thongTin);
            }

            if (response.lichSuImport) {
                hienLichSuImport(response.lichSuImport);
            }

            if (response.message) {
                alert(response.message);
            }

            if (response.ketQuaCungUng) {
                console.log(response.ketQuaCungUng);
                hienThiKetQuaCungUng(response.ketQuaCungUng);
            }
        },
        error: function(xhr, status, error) {
          console.log(error)
        }
          });
}

