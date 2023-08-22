document.addEventListener("DOMContentLoaded", function() {
    var tabNhapDuLieu = document.querySelector("#tabNhapDuLieu");
    tabNhapDuLieu.addEventListener("click", function(event) {
        var linkTabNhapDuLieu = document.querySelector("#tabNhapDuLieu > a");
        boChonTab(linkTabNhapDuLieu);
        document.querySelector("#nhapDuLieu").style.display = "block";
    });

    var tabDanhMuc = document.querySelector("#tabDanhMuc");
    tabDanhMuc.addEventListener("click", function(event) {
        boChonTab(tabDanhMuc);
    });

    var tabDanhMucThuoc = document.querySelector("#tabDanhMucThuoc");
    tabDanhMucThuoc.addEventListener("click", function(event) {
       data = {"message": "danhMucThuoc"};
       sendData(data);
       document.querySelector('#danhMucThuoc').style.display = 'block';

    });

    var tabDanhMucHoatChat = document.querySelector("#tabDanhMucHoatChat");
    tabDanhMucHoatChat.addEventListener("click", function(event) {
       data = {"message": "danhMucHoatChat"};
       sendData(data);
       document.querySelector('#danhMucHoatChat').style.display = 'block';

    });

    var tabTheoDoiCungUng = document.querySelector("#tabTheoDoiCungUng");
    tabTheoDoiCungUng.addEventListener("click", function(event) {
        var linkTheoDoiCungUng = document.querySelector("#tabTheoDoiCungUng > a");
        boChonTab(linkTheoDoiCungUng);
        document.querySelector("#theoDoiCungUng").style.display = "block";
        data = {"message": "theoDoiCungUng"};
        sendData(data);
    });

    var tabPhanTichSuDung = document.querySelector("#tabPhanTichSuDung");
    tabPhanTichSuDung.addEventListener("click", function(event) {
        var linkPhanTichSuDung = document.querySelector("#tabPhanTichSuDung > a");
        boChonTab(linkPhanTichSuDung);
        document.querySelector("#phanTichSuDung").style.display = "block";
    });

    var tabXayDungDanhMuc = document.querySelector("#tabXayDungDanhMuc");
    tabXayDungDanhMuc.addEventListener("click", function(event) {
        var linkXayDungDanhMuc = document.querySelector("#tabXayDungDanhMuc > a");
        boChonTab(linkXayDungDanhMuc);
    });
});

function boChonTab(element) {
    var linkElement = document.querySelector(".nav-link[aria-current='page']");
    linkElement.classList.remove('active');
    linkElement.removeAttribute("aria-current");

    element.classList.add('active');
    element.setAttribute("aria-current", "page");
    var contents = document.querySelectorAll(".content");
    for (let c of contents) {
        c.style.display = "none";
    }
}

function taiDuLieu() {
    var path = document.querySelector("#nhapDuLieu > input").value;
        if (!path.includes(":\\")) {
            alert("Vui lòng nhập đường dẫn chính xác.");
        } else if (!path.includes("xls")) {
            alert("Vui lòng nhập đường dẫn tới file Excel.");
        } else {
            data = {"path": path};
            sendData(data);
        }
}

function theoDoiCungUngThuoc() {
    var duongDan = document.querySelector('#theoDoiCungUng > input').value;
    if (duongDan === "") {
        alert("Vui lòng nhập đường dẫn tới thư mục.");
    } else {
        data = {"duongDan": duongDan};
        sendData(data);
    }

}

function sendData(data) {
    $.ajax({
        url: '/',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(response) {
            if (response.message) {
                document.querySelector(".alert").innerHTML = "Tải dữ liệu thành công!";
                document.querySelector(".alert").style.display = 'block';
            };

            if (response.danhMucThuoc) {
                hienThiDanhMucThuoc(response.danhMucThuoc);
            };

            if (response.danhMucHoatChat) {
                console.log(response.danhMucHoatChat);
                hienThiDanhMucHoatChat(response.danhMucHoatChat);
            }

            if (response.duongDan) {
                var input = document.querySelector('#theoDoiCungUng > input');
                input.value = response.duongDan;
            }

            if (response.loiDuongDan) {
                var alert = document.querySelector('#theoDoiCungUng > div');
                alert.innerHTML = response.loiDuongDan;
                alert.style.display = 'block';
            }
        },
        error: function(xhr, status, error) {
          console.log(error)
        }
          });
}

function hienThiDanhMucThuoc(danhMucThuoc) {
    var html = "";
    for (let row of danhMucThuoc) {
        html += `<tr id="${row[0]}" onclick="selectRow(${row[0]})">
            <th>${row[0]}</th>
            <td>${row[1]}</td>
            <td>${row[2]}</td>
        </tr>`;
    }
    document.getElementById('bodyDanhMucThuoc').innerHTML = html;
}

function hienThiDanhMucHoatChat(danhMucHoatChat) {
    var html = "";
    for (let row of danhMucHoatChat) {
        html += `<tr id="HC${row[0]}" onclick="selectRow('HC${row[0]}')">
            <th>${row[0]}</th>
            <td>${row[1]}</td>
        </tr>`;
    }
    document.getElementById('bodyDanhMucHoatChat').innerHTML = html;
}

function selectRow(n) {
    var row = document.getElementById(`${n}`);
    if (row.classList.contains("selected")) {
        row.classList.remove("selected");
    } else {
        row.classList.add("selected");
    }
}
