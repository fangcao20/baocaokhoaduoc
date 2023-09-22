import pandas as pd
import mysql.connector as connector
from datetime import datetime, timedelta

mydb = connector.connect(user='duocbenh_duocbenh', password='PhuongThao5=))',
                         host='112.213.89.194',
                         database='duocbenh_baocaokhoaduoc')
# mydb = connector.connect(user='root', password='Phiphi05',
#                          host='localhost',
#                          database='baocaokhoaduoc')


def capitalize_words(s):
    s = s.strip()
    return s


def checkkitu(input_string):
    if "%" in input_string:
        modified_string = input_string.replace("%", r"\%")
    else:
        modified_string = input_string
    return modified_string


def checkDanhMuc(record, col, danhmuc):
    mycursor = mydb.cursor()
    colCCH = col + 'CCH'
    record = checkkitu(str(record).lower())
    if 'danhmuc' in danhmuc:
        mycursor.execute(f"SELECT * FROM {danhmuc} WHERE LOWER({colCCH}) LIKE %s", (f"%;{record};%",))
    else:
        mycursor.execute(f'SELECT * FROM {danhmuc} where {col} = %s', (record,))
    results = mycursor.fetchall()
    if results:
        if danhmuc == 'danhmuchoatchatbenhvien':
            idHoatChat = results[0][0]
            mycursor.execute("update danhmuchoatchatbenhvien set maHoatChat = CONCAT('HC', LPAD(%s, 5, '0')) where "
                             "idHoatChat = %s and maHoatChat is null", (idHoatChat, idHoatChat))
        mycursor.close()
        return True
    else:
        mycursor.close()
        return False


def insertDanhMuc(index, data, colDB, danhmucDB):
    mycursor = mydb.cursor()
    colDBCCH = colDB + 'CCH'
    for row in data:
        record = capitalize_words(row[index])
        recordCCH = f';{record};'
        if not checkDanhMuc(record, colDB, danhmucDB):
            if danhmucDB != 'danhmuchoatchatbenhvien':
                mycursor.execute(f'insert into {danhmucDB}({colDB}, {colDBCCH}) values (%s, %s)', (record, recordCCH))
            else:
                mycursor.execute('select sttTT20 from danhmuchoatchattt20 where hoatChatTT20 = %s', (record,))
                result = mycursor.fetchall()
                if len(result) > 0:
                    sttTT20 = result[0][0]
                else:
                    sttTT20 = None
                mycursor.execute('''insert into danhmuchoatchatbenhvien (maHoatChat, sttTT20, hoatChat, hoatChatCCH)
                values (CONCAT('HC', LPAD(LAST_INSERT_ID(), 5, '0')), %s, %s, %s)''', (sttTT20, record, recordCCH))
    mydb.commit()
    mycursor.close()


def getId(record, colId, colName, danhmuc):
    colNameCCH = colName + 'CCH'
    mycursor = mydb.cursor()
    record = checkkitu(record)
    mycursor.execute(f'select {colId} from {danhmuc} where {colNameCCH} like %s', (f"%;{record};%",))
    result = mycursor.fetchall()
    mycursor.close()
    if not result:
        print(record, danhmuc, result)
    return result[0][0]


def nhapKetQuaTrungThau(dt, idLichSu):
    mycursor = mydb.cursor()
    maDotThau = dt['maDotThau']
    data = dt['data']
    mycursor.execute('select idDotThau from danhmucdotthau where maDotThau = %s', (maDotThau,))
    idDotThau = mycursor.fetchall()[0][0]

    insertDanhMuc(1, data, 'tenThuoc', 'danhmucthuoc')
    insertDanhMuc(2, data, 'hoatChat', 'danhmuchoatchatbenhvien')
    insertDanhMuc(3, data, 'hamLuong', 'danhmuchamluong')
    insertDanhMuc(4, data, 'soDangKy', 'danhmucsodangky')
    insertDanhMuc(5, data, 'duongDung', 'danhmucduongdung')
    insertDanhMuc(6, data, 'dangBaoChe', 'danhmucdangbaoche')
    insertDanhMuc(7, data, 'quyCachDongGoi', 'danhmucquycachdonggoi')
    insertDanhMuc(8, data, 'donViTinh', 'danhmucdonvitinh')
    insertDanhMuc(9, data, 'coSoSanXuat', 'danhmuccososanxuat')
    insertDanhMuc(10, data, 'nuocSanXuat', 'danhmucnuocsanxuat')
    insertDanhMuc(11, data, 'nhaThau', 'danhmucnhathau')
    insertDanhMuc(12, data, 'nhomThau', 'danhmucnhomthau')

    for row in data:
        idThuoc = getId(capitalize_words(row[1]), 'idThuoc', 'tenThuoc', 'danhmucthuoc')
        idHoatChat = getId(capitalize_words(row[2]), 'idHoatChat', 'hoatChat', 'danhmuchoatchatbenhvien')
        idHamLuong = getId(capitalize_words(row[3]), 'idHamLuong', 'hamLuong', 'danhmuchamluong')
        idSDK = getId(capitalize_words(row[4]), 'idSDK', 'soDangKy', 'danhmucsodangky')
        idDuongDung = getId(capitalize_words(row[5]), 'idDuongDung', 'duongDung', 'danhmucduongdung')
        idDangBaoChe = getId(capitalize_words(row[6]), 'idDangBaoChe', 'dangBaoChe', 'danhmucdangbaoche')
        idQuyCachDongGoi = getId(capitalize_words(row[7]), "idQuyCachDongGoi", 'quyCachDongGoi',
                                 'danhmucquycachdonggoi')
        idDonViTinh = getId(capitalize_words(row[8]), "idDonViTinh", 'donViTinh', 'danhmucdonvitinh')
        idCoSoSanXuat = getId(capitalize_words(row[9]), 'idCoSoSanXuat', 'coSoSanXuat',
                              'danhmuccososanxuat')
        idNuocSanXuat = getId(capitalize_words(row[10]), "idNuocSanXuat", 'nuocSanXuat',
                              'danhmucnuocsanxuat')
        idNhaThau = getId(capitalize_words(row[11]), "idNhaThau", 'nhaThau', 'danhmucnhathau')
        idNhomThau = getId(capitalize_words(row[12]), "idNhomThau", 'nhomThau', 'danhmucnhomthau')

        mycursor.execute('select sttTT20 from danhmuchoatchatbenhvien where idHoatChat = %s', (idHoatChat,))
        result = mycursor.fetchall()
        if len(result) > 0 and result[0][0] is not None:
            sttTT20 = result[0][0]
            mycursor.execute('select idNhomDuocLyCap1, idNhomHoaDuoc1 from danhmuchoatchattt20 where sttTT20 = %s',
                             (sttTT20,))
            idNhomDuocLyCap1, idNhomHoaDuoc1 = mycursor.fetchall()[0]
        else:
            idNhomDuocLyCap1 = None
            idNhomHoaDuoc1 = None
        soLuong = float(row[13].replace(',', ''))
        donGia = float(row[14].replace(',', ''))
        thanhTien = float(row[15].replace(',', ''))

        values = (idThuoc, idHoatChat, idNhomDuocLyCap1, idNhomHoaDuoc1, idHamLuong, idSDK, idDuongDung, idDangBaoChe,
                  idQuyCachDongGoi, idDonViTinh, idCoSoSanXuat, idNuocSanXuat, idNhaThau, idNhomThau, soLuong, donGia,
                  thanhTien, idDotThau, idLichSu)

        mycursor.execute('''insert into ketquatrungthau(idThuoc, idHoatChat, idNhomDuocLyCap1, idNhomHoaDuoc1, 
        idHamLuong, idSDK, idDuongDung, idDangBaoChe, idQuyCachDongGoi, idDonViTinh, idCoSoSanXuat, 
        idNuocSanXuat, idNhaThau, idNhomThau, soLuong, donGia, thanhTien, idDotThau, idLichSu) values (%s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                         values)
    mycursor.close()
    mydb.commit()


def getValue(id, idCol, colName, danhmuc):
    mycursor = mydb.cursor()
    mycursor.execute(f'select {colName} from {danhmuc} where {idCol} = %s', (id,))
    result = mycursor.fetchall()
    mycursor.close()
    if len(result) > 0:
        return result[0][0]
    else:
        return None


def xuatKetQuaTrungThau():
    mycursor = mydb.cursor()
    mycursor.execute('select * from ketquatrungthau')
    results = mycursor.fetchall()
    ketQuaList = []
    columnNames = ['Tên thuốc', 'Hoạt chất', 'Nhóm Dược lý', 'Nhóm Hóa dược', 'Hàm lượng', 'SĐK',
                   'Đường dùng', 'Dạng bào chế', 'Quy cách đóng gói', 'ĐVT', 'Cơ sở sản xuất', 'Nước sản xuất',
                   'Nhà thầu trúng thầu', 'Nhóm thầu', 'Gói mua sắm', 'Số lượng', 'Đơn giá', 'Thành tiền',
                   'Đợt thầu', 'Số QĐ', 'Ngày QĐ', 'Ngày hết hạn', 'Tên Bệnh viện']
    for row in results:
        ketQuaDict = {}
        idThuoc = getValue(row[1], 'idThuoc', 'tenThuoc', 'danhmucthuoc')
        idHoatChat = getValue(row[2], 'idHoatChat', 'hoatChat', 'danhmuchoatchatbenhvien')
        idNhomDuocLy = getValue(row[3], 'idNhomDuocLyCap1', 'nhomDuocLyCap1', 'danhmucnhomduoclycap1')
        idNhomHoaDuoc = getValue(row[4], 'idNhomHoaDuoc1', 'nhomHoaDuoc1', 'danhmucnhomhoaduoc1')
        idHamLuong = getValue(row[5], 'idHamLuong', 'hamLuong', 'danhmuchamluong')
        idSDK = getValue(row[6], 'idSDK', 'soDangKy', 'danhmucsodangky')
        idDuongDung = getValue(row[7], 'idDuongDung', 'duongDung', 'danhmucduongdung')
        idDangBaoChe = getValue(row[8], 'idDangBaoChe', 'dangBaoChe', 'danhmucdangbaoche')
        idQuyCachDongGoi = getValue(row[9], "idQuyCachDongGoi", 'quyCachDongGoi', 'danhmucquycachdonggoi')
        idDonViTinh = getValue(row[10], "idDonViTinh", 'donViTinh', 'danhmucdonvitinh')
        idCoSoSanXuat = getValue(row[11], 'idCoSoSanXuat', 'coSoSanXuat', 'danhmuccososanxuat')
        idNuocSanXuat = getValue(row[12], "idNuocSanXuat", 'nuocSanXuat', 'danhmucnuocsanxuat')
        idNhaThau = getValue(row[13], "idNhaThau", 'nhaThau', 'danhmucnhathau')
        idNhomThau = getValue(row[14], "idNhomThau", 'nhomThau', 'danhmucnhomthau')
        # soLuong = locale.format_string('%d', row[15], grouping=True)
        # donGia = locale.format_string('%d', row[16], grouping=True)
        # thanhTien = locale.format_string('%d', row[17], grouping=True)
        soLuong = row[15]
        donGia = row[16]
        thanhTien = row[17]
        idDotThau = getValue(row[18], "idDotThau", 'maDotThau', 'danhmucdotthau')

        mycursor.execute(
            'select tenBenhVien, maDotThau, goiMuaSam, soQD, ngayQD, ngayHetHan from danhmucdotthau where maDotThau = %s',
            (idDotThau,))
        tenBenhVien, maDotThau, goiMuaSam, soQD, ngayQD, ngayHetHan = mycursor.fetchall()[0]

        values = [idThuoc, idHoatChat, idNhomDuocLy,
                  idNhomHoaDuoc, idHamLuong, idSDK, idDuongDung, idDangBaoChe, idQuyCachDongGoi,
                  idDonViTinh, idCoSoSanXuat, idNuocSanXuat, idNhaThau, idNhomThau, goiMuaSam, soLuong, donGia,
                  thanhTien,
                  maDotThau, soQD, str(ngayQD), str(ngayHetHan), tenBenhVien]

        for i in range(len(values)):
            ketQuaDict[columnNames[i]] = values[i]

        ketQuaList.append(ketQuaDict)
    mycursor.close()
    return ketQuaList


danhMucList = ['danhmucthuoc', 'danhmuchoatchatbenhvien', 'danhmucnhomduoclycap1', 'danhmucnhomhoaduoc1',
               'danhmuchamluong', 'danhmucduongdung', 'danhmucdangbaoche', 'danhmucquycachdonggoi',
               'danhmucdonvitinh', 'danhmuccososanxuat', 'danhmucnuocsanxuat', 'danhmucnhathau', 'danhmucnhomthau',
               'danhmucdotthau']

idList = ['idThuoc', 'idHoatChat', 'idNhomDuocLyCap1', 'idNhomHoaDuoc1', 'idHamLuong', 'idDuongDung',
          'idDangBaoChe', 'idQuyCachDongGoi', 'idDonViTinh', 'idCoSoSanXuat', 'idNuocSanXuat', 'idNhaThau',
          'idNhomThau', 'idDotThau']

colNameList = ['tenThuoc', 'hoatChat', 'nhomDuocLyCap1', 'nhomHoaDuoc1', 'hamLuong', 'duongDung', 'dangBaoChe',
               'quyCachDongGoi', 'donViTinh', 'coSoSanXuat', 'nuocSanXuat', 'nhaThau', 'nhomThau', 'maDotThau']


def xuatDanhMuc():
    mycursor = mydb.cursor()
    danhMucDict = {}
    for i in range(len(danhMucList)):
        dm = danhMucList[i]
        colName = colNameList[i]
        idCol = idList[i]

        if dm != "danhmuchoatchatbenhvien" and dm != 'danhmucnhomduoclycap1' and dm != 'danhmucdotthau':
            mycursor.execute(f'select {idCol}, {colName} from {dm} order by {colName}')
        elif dm == 'danhmucdotthau':
            mycursor.execute(f'select * from {dm}')
        elif dm == 'danhmucnhomduoclycap1':
            mycursor.execute(f'select {idCol}, {colName} from {dm}')
        elif dm == 'danhmuchoatchatbenhvien':
            mycursor.execute('''
                SELECT
                    b.idHoatChat, b.maHoatChat, b.sttTT20, b.hoatChat,
                    nh1.nhomDuocLyCap1,
                    nh2.nhomHoaDuoc1
                FROM danhmuchoatchatbenhvien AS b
                LEFT JOIN danhmucnhomduoclycap1 AS nh1 ON b.idNhomDuocLyCap1 = nh1.idNhomDuocLyCap1
                LEFT JOIN danhmucnhomhoaduoc1 AS nh2 ON b.idNhomHoaDuoc1 = nh2.idNhomHoaDuoc1
                ORDER BY b.hoatChat
            ''')

        result = mycursor.fetchall()
        danhMucDict[dm] = result
    return danhMucDict


def gopDuLieu(data):
    mycursor = mydb.cursor()
    danhmuc = data['danhmuc']
    rowIdList = data['rowIdList']
    gopHoatChat = data['gopHoatChat']
    index = danhMucList.index(danhmuc)
    idCol = idList[index]
    colCCH = colNameList[index] + 'CCH'
    lastID = rowIdList[-1]
    mycursor.execute(f'select {colCCH} from {danhmuc} where {idCol} = %s', (lastID,))
    colCCH_value_lastID = mycursor.fetchall()[0][0]

    if 'sttTT20' not in gopHoatChat:
        for i in range(len(rowIdList) - 1):
            mycursor.execute(f'update ketquatrungthau set {idCol} = %s where {idCol} = %s', (lastID, rowIdList[i]))
            mycursor.execute(f'select {colCCH} from {danhmuc} where {idCol} = %s', (rowIdList[i],))
            colCCH_value = mycursor.fetchall()
            colCCH_value_lastID += f';{colCCH_value};'
            mycursor.execute(f'delete from {danhmuc} where {idCol} = %s', (rowIdList[i],))
        mycursor.execute(f'update {danhmuc} set {colCCH} = %s where {idCol} = %s', (colCCH_value_lastID, lastID))
    else:
        maHoatChat = gopHoatChat['maHoatChat']
        sttTT20 = gopHoatChat['sttTT20']
        mycursor.execute('select idNhomDuocLyCap1, idNhomHoaDuoc1 from danhmuchoatchattt20 where sttTT20 = %s',
                         (sttTT20,))
        idNhomDuocLyCap1, idNhomHoaDuoc1 = mycursor.fetchall()[0]
        idRowSTTTT20 = gopHoatChat['idRowSTTTT20']
        mycursor.execute(f'select {colCCH} from {danhmuc} where {idCol} = %s', (idRowSTTTT20,))
        colCCH_value_idRowSTTTT20 = mycursor.fetchall()[0][0]
        for i in range(len(rowIdList)):
            mycursor.execute(f'update ketquatrungthau set {idCol} = %s, idNhomDuocLyCap1 = %s, idNhomHoaDuoc1 = %s '
                             f'where {idCol} = %s', (idRowSTTTT20, idNhomDuocLyCap1, idNhomHoaDuoc1, rowIdList[i]))
            if rowIdList[i] != idRowSTTTT20:
                mycursor.execute(f'select {colCCH} from {danhmuc} where {idCol} = %s', (rowIdList[i],))
                colCCH_value = mycursor.fetchall()
                colCCH_value_idRowSTTTT20 += f';{colCCH_value};'
                mycursor.execute('delete from danhmuchoatchatbenhvien where idHoatChat = %s', (rowIdList[i],))
        mycursor.execute('update danhmuchoatchatbenhvien set maHoatChat = %s, hoatChatCCH = %s where idHoatChat = %s',
                         (maHoatChat, colCCH_value_idRowSTTTT20, idRowSTTTT20))
    mydb.commit()
    mycursor.close()


def saveFileInfo(files, dates):
    mycursor = mydb.cursor()
    for i in range(len(dates)):
        name = files[i].filename
        date = dates[i]
        file = files[i]
        if not checkDanhMuc(name, 'fileName', 'fileinfo'):
            mycursor.execute('insert into fileinfo(fileName, modifiedDate) values (%s, %s)', (name, date))
            idFile = mycursor.lastrowid
            if not nhapDuLieuKho(idFile, file):
                mycursor.execute('delete from fileinfo where idFile = %s', (idFile,))
        else:
            mycursor.execute('select idFile, modifiedDate from fileinfo where fileName = %s', (name,))
            idFile, modifiedDate = mycursor.fetchall()[0]
            if modifiedDate != date:
                mycursor.execute('update fileinfo set modifiedDate = %s where fileName = %s', (date, name))
                nhapDuLieuKho(idFile, file)
    mydb.commit()
    mycursor.close()


def nhapDuLieuKho(idFile, file):
    mycursor = mydb.cursor()
    df = pd.read_excel(file)
    df = df.where(pd.notna(df), None)
    headers = df.columns.tolist()
    tenThuoc = headers[2].split(' : ')[1].strip().lower()
    mycursor.execute('select idThuoc from danhmucthuoc where lower(tenThuoc) = %s', (tenThuoc,))
    result = mycursor.fetchall()
    if result:
        idThuoc = result[0][0]
        if "kho chẵn" in file.filename.lower():
            insertKho(df, "khochan", idThuoc, idFile)
        else:
            insertKho(df, "khole", idThuoc, idFile)
        mycursor.close()
        return True
    else:
        print(f'Không có thuốc {tenThuoc} trong danhmuc')
        mycursor.close()
        return False


def insertKho(df, loaikho, idThuoc, idFile):
    mycursor = mydb.cursor()
    mycursor.execute(f'delete from {loaikho} where idFile = %s', (idFile,))
    for i in range(2, df.shape[0] - 1):
        row = df.iloc[i].tolist()
        ngay = row[0]
        nhap = int(row[4])
        ton = int(row[6])
        xuat = int(row[5])
        mycursor.execute(
            f"insert into {loaikho}(idFile, ngay, idThuoc, nhap, xuat, ton) values (%s, %s, %s, %s, %s, %s)",
            (idFile, ngay, idThuoc, nhap, xuat, ton))
    mydb.commit()
    mycursor.close()


def mergeDuLieuKho():
    mycursor = mydb.cursor()
    mycursor.execute('truncate table tonghopthau')
    mycursor.execute('truncate table thongkekho')

    mycursor.execute('select distinct idThuoc from khochan')
    results = mycursor.fetchall()
    idThuocList = [r[0] for r in results]
    for idThuoc in idThuocList:
        if checkDanhMuc(idThuoc, 'idThuoc', 'khole'):
            try:
                mycursor.execute('select sum(soLuong) from ketquatrungthau where idThuoc = %s', (idThuoc,))
                tongKeHoach = mycursor.fetchall()[0][0]
                print(idThuoc, tongKeHoach)
                mycursor.execute('''
                    select dt.ngayQD 
                    from ketquatrungthau as kq
                    left join danhmucdotthau as dt on kq.idDotThau = dt.idDotThau
                    where kq.idThuoc = %s
                    order by dt.ngayQD desc limit 1;
                ''', (idThuoc,))
                ngayThau = mycursor.fetchall()[0][0]
                print(ngayThau)
                # Bảng Thống kê kho
                duTruConLai = tongKeHoach
                mycursor.execute('select ngay, nhap from khochan where idThuoc = %s and nhap > 0', (idThuoc,))
                results = mycursor.fetchall()
                ngayNhapChanList = []
                nhapChanList = []
                sumNhapChan = 0
                nhapChanCungNgay = 0
                trungBinhNhapChan = 0
                for r in results:
                    nhapChanList.append(r[1])
                    ngayNhapChanList.append(r[0])
                mycursor.execute('select ngay, ton from khole where idThuoc = %s', (idThuoc,))
                results = mycursor.fetchall()
                tonLeList = []
                ngayTonLeList = []
                soLanNhap = 0
                for r in results:
                    tonLeList.append(r[1])
                    ngayTonLeList.append(r[0])
                for i in range(len(ngayNhapChanList)):
                    ngay = ngayNhapChanList[i]
                    nhap = nhapChanList[i]
                    nhapChanCungNgay += nhap
                    if i < len(ngayNhapChanList) - 1:
                        if ngay == ngayNhapChanList[i + 1]:
                            continue
                        else:
                            nhap = nhapChanCungNgay
                            soLanNhap += 1
                            nhapChanCungNgay = 0
                    else:
                        soLanNhap = len(set(ngayNhapChanList))
                    sumNhapChan += nhap
                    trungBinhNhapChan = int(round(sumNhapChan / soLanNhap, 0))

                    ngayNhapChan = ngay
                    if ngay <= ngayTonLeList[0]:
                        tonLe = 0
                        closest_date = ngay
                    elif ngay in ngayTonLeList:
                        index = ngayTonLeList.index(ngay) - 1
                        closest_date = ngayTonLeList[index]
                        tonLe = tonLeList[index]
                    else:
                        while ngay not in ngayTonLeList:
                            ngay = ngay - timedelta(days=1)
                        index = None
                        for idx in range(len(ngayTonLeList) - 1, -1, -1):
                            if ngayTonLeList[idx] == ngay:
                                index = idx
                                break

                        closest_date = ngayTonLeList[index]
                        tonLe = tonLeList[index]
                    duTruConLai -= nhap
                    mycursor.execute('''insert into thongkekho(ngayNhapChan, idThuoc, nhapChan, tonLeTruocNhapChan,
                    trungBinhNhapChan, duTruConLai) values (%s, %s, %s, %s, %s, %s)''',
                                     (ngayNhapChan, idThuoc, nhap, tonLe, trungBinhNhapChan, duTruConLai))
                    # Bảng Danh sách thầu

                mycursor.execute('select sum(nhap) from khochan where idThuoc = %s', (idThuoc,))
                tongSuDung = mycursor.fetchall()[0][0]
                conLai = tongKeHoach - tongSuDung
                mycursor.execute('select ton from khole where idThuoc = %s order by ngay desc limit 1', (idThuoc,))
                tonLeCuoiCung = mycursor.fetchall()[0][0]
                mycursor.execute('select nhap from khole where idThuoc = %s and nhap > 0 order by ngay desc limit 1',
                                 (idThuoc,))
                nhapLeCuoiCung = mycursor.fetchall()[0][0]
                soLanDuTru = round(conLai / trungBinhNhapChan, 2)
                mycursor.execute('''insert into tonghopthau(ngayThau, idThuoc, tongKeHoach, tongSuDung, conLai, nhapLeCuoiCung,
                tonLeCuoiCung, trungBinhNhapChanCuoiCung, soLanDuTru) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                 (ngayThau, idThuoc, tongKeHoach, tongSuDung, conLai, nhapLeCuoiCung, tonLeCuoiCung,
                                  trungBinhNhapChan, soLanDuTru))
            except Exception as e:
                print(e, idThuoc)

    mydb.commit()
    mycursor.close()


def checkNaN(x):
    if str(x) == 'nan':
        return ''
    else:
        return x


def nhapDuLieuABCVEN(file):
    mycursor = mydb.cursor()
    mycursor.execute('truncate table dulieuabcven')
    df = pd.read_excel(file)
    df = df.where(pd.notna(df), None)

    tongTien = df['Thành tiền'].sum()

    for i in range(df.shape[0]):
        row = df.iloc[i].tolist()
        tenThuoc = row[0]
        hoatChat = row[1]
        bietDuoc = checkNaN(row[2])
        generic = checkNaN(row[3])
        ven = row[4]
        nuocSanXuat = row[5]
        maATC = checkNaN(row[6])
        donViTinh = row[7]
        soLuong = int(row[8])
        donGia = int(row[9])
        thanhTien = int(row[10])
        phanTramTongTien = thanhTien / tongTien
        phanTramSoLuong = 1 / df.shape[0]
        mycursor.execute('''insert into dulieuabcven(tenThuoc, hoatChat, bietDuoc, generic, ven, nuocSanXuat, maATC, 
        donViTinh, soLuong, donGia, thanhTien, phanTramTongTien, phanTramSoLuong) values (%s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s)''',
                         (tenThuoc, hoatChat, bietDuoc, generic, ven, nuocSanXuat, maATC,
                          donViTinh, soLuong, donGia, thanhTien, phanTramTongTien, phanTramSoLuong))
    mydb.commit()

    mycursor.execute('select * from dulieuabcven order by phanTramTongTien desc')
    results = mycursor.fetchall()
    phanTramTichLuyTongTien = 0
    xepHangABC = 0
    phanTramSoLuongTichLuy = 0
    for row in results:
        phanTramTongTien = row[12]
        phanTramSoLuong = row[18]
        phanTramTichLuyTongTien += phanTramTongTien
        xepHangABC += 1
        phanTramSoLuongTichLuy += phanTramSoLuong
        if phanTramTichLuyTongTien < 0.75:
            nhomABC = 'A'
        elif phanTramTichLuyTongTien < 0.9:
            nhomABC = 'B'
        else:
            nhomABC = 'C'
        ven = row[5]
        gopABCVEN = nhomABC + ven
        if gopABCVEN in ['AV', 'AE', 'AN', 'BV', 'CV']:
            ABCVENmatrix = 'I'
        elif gopABCVEN in ['BE', 'BN', 'CE']:
            ABCVENmatrix = 'II'
        else:
            ABCVENmatrix = 'III'
        rowID = row[0]
        mycursor.execute('''update dulieuabcven set phanTramTichLuyTongTien = %s, phanTramSoLuongTichLuy = %s,
        xepHangABC = %s, nhomABC = %s, gopABCVEN = %s, ABCVENmatrix = %s where id = %s''',
                         (phanTramTichLuyTongTien, phanTramSoLuongTichLuy, xepHangABC, nhomABC, gopABCVEN, ABCVENmatrix,
                          rowID))
    mydb.commit()
    mycursor.close()


def suaDanhMuc(data):
    mycursor = mydb.cursor()
    dm = data[-1]
    index = danhMucList.index(dm)
    idCol = idList[index]
    for item in data[:-1]:
        rowID = int(item['id'])
        newValue = item['newValue']
        mycursor.execute(f'SHOW COLUMNS FROM {dm}')
        contentCol = mycursor.fetchall()[1][0]

        mycursor.execute(f'update {dm} set {contentCol} = %s where {idCol} = %s', (newValue, rowID))
    mydb.commit()
    mycursor.close()


def nhapDotThau(data):
    mycursor = mydb.cursor()
    value = []
    for i in range(len(data)):
        value.append(data[i])

    mycursor.execute('insert into danhmucdotthau(maDotThau, tenDotThau, giaiDoan, hinhThucDauThau, goiMuaSam, soQD, '
                     'ngayQD, ngayHetHan, tenBenhVien, ghiChu) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', value)
    mydb.commit()
    mycursor.close()


def selectDotThau(*args):
    colName = args[0]
    mycursor = mydb.cursor()
    mycursor.execute(f'select distinct({colName}) from danhmucdotthau')
    results = mycursor.fetchall()
    mycursor.close()
    return [x[0] for x in results]


def convert(date_time):
    date_obj = datetime.strptime(date_time, '%Y-%m-%d')
    return date_obj


def updateDotThau(data):
    mycursor = mydb.cursor()
    if data['type'] == 'update':
        data['data'][6] = convert(data['data'][6])
        data['data'][7] = convert(data['data'][7])
        data['data'].append(data['idDotThau'])
        mycursor.execute('''update danhmucdotthau set maDotThau = %s, tenDotThau = %s, giaiDoan = %s,
        hinhThucDauThau = %s, goiMuaSam = %s, soQD = %s, ngayQD = %s, ngayHetHan = %s, tenBenhVien = %s, ghiChu = %s
        where idDotThau = %s''', data['data'])
    else:
        mycursor.execute('delete from danhmucdotthau where idDotThau = %s', (data['idDotThau'],))
    mydb.commit()
    mycursor.close()


def thongTinTheoMaDotThau(maDotThau):
    mycursor = mydb.cursor()
    mycursor.execute('select * from danhmucdotthau where maDotThau = %s', (maDotThau,))
    result = mycursor.fetchall()
    mycursor.close()
    return result[0]


def xuatLichSuImport():
    mycursor = mydb.cursor()
    mycursor.execute('select * from lichsuimport order by thoiGianImport desc')
    results = mycursor.fetchall()
    lichSuImport = []
    for rs in results:
        rs = list(rs)
        idDotThau = rs[1]
        mycursor.execute('select maDotThau from danhmucdotthau where idDotThau = %s', (idDotThau,))
        maDotThau = mycursor.fetchall()[0][0]
        rs[1] = maDotThau
        lichSuImport.append(rs)
    mycursor.close()
    return lichSuImport


def xoaDuLieuImport(idLichSu):
    mycursor = mydb.cursor()
    mycursor.execute('delete from lichsuimport where idLichSu = %s', (idLichSu,))
    mydb.commit()
    mycursor.close()


def nhapLichSuImport(data):
    maDotThau = data['maDotThau']
    mycursor = mydb.cursor()
    mycursor.execute('select idDotThau from danhmucdotthau where maDotThau = %s', (maDotThau,))
    idDotThau = mycursor.fetchall()[0][0]
    thoiGianImport = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    mycursor.execute('insert into lichsuimport (idDotThau, thoiGianImport) values (%s, %s)',
                     (idDotThau, thoiGianImport))
    idLichSu = mycursor.lastrowid
    mydb.commit()
    mycursor.close()
    return idLichSu


def theoDoiCungUng():
    mycursor = mydb.cursor()
    ketQua = {}
    danhsachthaulist = []
    mycursor.execute('''
    with last_kqs as (select * from ketquatrungthau where idKetQua in (select max(idKetQua) from ketquatrungthau group by idThuoc))

    SELECT th.ngayThau, th.tongKeHoach, th.tongSuDung, th.conLai, th.nhapLeCuoiCung, th.tonLeCuoiCung, th.trungBinhNhapChanCuoiCung, th.soLanDuTru,
            t.idThuoc, t.tenThuoc, hc.hoatChat, dl.nhomDuocLyCap1, hd.nhomHoaDuoc1, nt.nhomThau
            FROM tonghopthau as th
            left join danhmucthuoc as t on th.idThuoc = t.idThuoc
            left join last_kqs AS kq on th.idThuoc = kq.idThuoc
            left join danhmuchoatchatbenhvien as hc on kq.idHoatChat = hc.idHoatChat
            left join danhmucnhomduoclycap1 as dl on hc.idNhomDuocLyCap1 = dl.idNhomDuocLyCap1
            left join danhmucnhomhoaduoc1 as hd on hc.idNhomHoaDuoc1 = hd.idNhomHoaDuoc1
            left join danhmucnhomthau as nt on kq.idNhomThau = nt.idNhomThau
    ''')
    ketQua['danhsachthau'] = mycursor.fetchall()

    mycursor.execute('''
        SELECT
            DATE_FORMAT(ngayNhapChan, '%Y-%m') as month,
            t.tenThuoc,
            SUM(tk.nhapChan) AS nhapChanTheoThang
        FROM thongkekho as tk
        left join danhmucthuoc as t on t.idThuoc = tk.idThuoc
        GROUP BY tk.idThuoc, DATE_FORMAT(ngayNhapChan, '%Y-%m')
        ORDER BY tk.idThuoc, STR_TO_DATE(month, '%Y/%m')
            ''')
    ketQua['suDungTheoThang'] = mycursor.fetchall()

    mycursor.execute('''
        WITH LastestDates AS ( SELECT th.idThuoc, MAX(dt.ngayQD) AS maxNgayQD 
        FROM tonghopthau AS th LEFT JOIN ketquatrungthau AS kq ON kq.idThuoc = th.idThuoc 
        LEFT JOIN danhmucdotthau AS dt ON dt.idDotThau = kq.idDotThau GROUP BY th.idThuoc ) 
        SELECT t.tenThuoc, hc.hoatChat, kq.soLuong, dt.ngayQD FROM tonghopthau AS th 
        LEFT JOIN danhmucthuoc AS t ON t.idThuoc = th.idThuoc 
        LEFT JOIN ketquatrungthau AS kq ON kq.idThuoc = th.idThuoc 
        LEFT JOIN danhmuchoatchatbenhvien AS hc ON kq.idHoatChat = hc.idHoatChat 
        LEFT JOIN danhmucdotthau AS dt ON dt.idDotThau = kq.idDotThau 
        WHERE (th.idThuoc, dt.ngayQD) IN (SELECT idThuoc, maxNgayQD FROM LastestDates);''')
    ketQua['danhsachthuoc'] = mycursor.fetchall()

    mycursor.execute('select * from thongkekho')
    ketQua['thongkekho'] = mycursor.fetchall()
    mycursor.close()
    return ketQua
