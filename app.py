from flask import Flask, render_template, request, jsonify
from database import nhapKetQuaTrungThau, xuatKetQuaTrungThau, xuatDanhMuc, gopDuLieu, saveFileInfo, mergeDuLieuKho, \
    nhapDuLieuABCVEN, suaDanhMuc, nhapDotThau, selectDotThau, updateDotThau, thongTinTheoMaDotThau, \
    xuatLichSuImport, nhapLichSuImport, xoaDuLieuImport

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        dt = request.get_json()
        if 'start' in dt:
            danhMucDotThau = xuatDanhMuc()['danhmucdotthau']
            ketQuaList = xuatKetQuaTrungThau()
            maDotThau = selectDotThau('maDotThau')
            lichSuImport = xuatLichSuImport()
            return jsonify(ketQuaList=ketQuaList, danhMucDotThau=danhMucDotThau, maDotThau=maDotThau,
                           lichSuImport=lichSuImport)
        if 'dm' in dt:
            danhMucDict = xuatDanhMuc()
            return jsonify(danhMucDict=danhMucDict)
        if 'gopDuLieu' in dt:
            data = dt['gopDuLieu']
            gopDuLieu(data)
            danhMucDict = xuatDanhMuc()
            ketQuaList = xuatKetQuaTrungThau()
            return jsonify(danhMucDict=danhMucDict, ketQuaList=ketQuaList)
        if 'cungung' in dt:
            mergeDuLieuKho()
        if 'suaDanhMuc' in dt:
            data = dt['suaDanhMuc']
            dm = data[-1]
            suaDanhMuc(data)
            danhMucList = xuatDanhMuc()
            ketQuaList = xuatKetQuaTrungThau()
            return jsonify(danhMucList=danhMucList, ketQuaList=ketQuaList)
        if 'dataDotThau' in dt:
            data = dt['dataDotThau']
            nhapDotThau(data)
            danhMucDotThau = xuatDanhMuc()['danhmucdotthau']
            return jsonify(danhMucDotThau=danhMucDotThau)
        if 'dataUpdateDotThau' in dt:
            updateDotThau(dt['dataUpdateDotThau'])
            danhMucDotThau = xuatDanhMuc()['danhmucdotthau']
            return jsonify(danhMucDotThau=danhMucDotThau)
        if 'chonMaDotThau' in dt:
            maDotThau = dt['chonMaDotThau']
            thongTin = thongTinTheoMaDotThau(maDotThau)
            return jsonify(thongTin=thongTin)
        if 'luuChiTietThuoc' in dt:
            data = dt['luuChiTietThuoc']
            idLichSu = nhapLichSuImport(data)
            nhapKetQuaTrungThau(data, idLichSu)
            ketQuaList = xuatKetQuaTrungThau()
            lichSuImport = xuatLichSuImport()
            return jsonify(ketQuaList=ketQuaList, lichSuImport=lichSuImport)
        if 'xoaDuLieuImport' in dt:
            xoaDuLieuImport(dt['xoaDuLieuImport'])
            lichSuImport = xuatLichSuImport()
            ketQuaList = xuatKetQuaTrungThau()
            return jsonify(lichSuImport=lichSuImport, ketQuaList=ketQuaList)
    return render_template('index.html')


@app.route('/files', methods=['POST', 'GET'])
def uploadfiles():
    if request.method == 'POST':
        if request.form.getlist('date'):
            files = request.files.getlist('files')
            dates = request.form.getlist('date')
            saveFileInfo(files, dates)
        else:
            file = request.files.get('file')
            nhapDuLieuABCVEN(file)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
