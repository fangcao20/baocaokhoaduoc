from flask import Flask, render_template, request, jsonify
from main import nhapDuLieuTrungThau, layDanhMucThuoc, layDanhMucHoatChat, layDuongDan, checkDuongDan
from main import nhapDuLieuKhoChan, nhapDuLieuKhoLe, mergeDuLieu

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        dt = request.get_json()
        if "path" in dt:
            path = dt['path']
            nhapDuLieuTrungThau(path)
            return jsonify({"message": "success"})
        elif "message" in dt:
            if dt["message"] == "danhMucThuoc":
                danhMucThuoc = layDanhMucThuoc()
                return jsonify(danhMucThuoc=danhMucThuoc)
            elif dt["message"] == "danhMucHoatChat":
                danhMucHoatChat = layDanhMucHoatChat()
                return jsonify(danhMucHoatChat=danhMucHoatChat)
            elif dt["message"] == "theoDoiCungUng":
                duongDan = layDuongDan()
                return jsonify(duongDan=duongDan)
        elif "duongDan" in dt:
            newDuongDan = dt["duongDan"]
            newDuongDan = newDuongDan.replace('"', '')
            newDuongDan = newDuongDan.replace('\\', '/')
            message = checkDuongDan(newDuongDan)
            if message != "Success":
                return jsonify(loiDuongDan=message)
            else:
                nhapDuLieuKhoChan(newDuongDan)
                nhapDuLieuKhoLe(newDuongDan)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
