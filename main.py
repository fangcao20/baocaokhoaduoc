import pandas as pd
import mysql.connector as connector
from datetime import datetime, timedelta
import os

mydb = connector.connect(user='root', password='Phiphi05',
                         host='localhost',
                         database='baocaokhoaduoc')

mycursor = mydb.cursor()


def capitalize_words(s):
    s = s.strip()
    words = s.split()
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)


def nhapDuLieuTrungThau(path):
    path = path.replace('"', '')
    path = path.replace("\\", "/")
    df = pd.read_excel(path)
    df = df.where(pd.notna(df), None)
    maThau = df.iloc[:, 1].tolist()
    soQD = df.iloc[:, 17].tolist()
    ngayQD = df.iloc[:, 18].tolist()
    ngayHetHan = df.iloc[:, 19].tolist()
    hoatChat = df.iloc[:, 2].tolist()
    tenThuoc = df.iloc[:, 3].tolist()
    hamLuong = df.iloc[:, 4].tolist()
    duongDung = df.iloc[:, 5].tolist()
    dangBaoChe = df.iloc[:, 6].tolist()
    dangTrinhBay = df.iloc[:, 7].tolist()
    donviTinh = df.iloc[:, 8].tolist()
    hangSX = df.iloc[:, 9].tolist()
    nuocSX = df.iloc[:, 10].tolist()
    soDK = df.iloc[:, 11].tolist()
    giaTrungThau = df.iloc[:, 12].tolist()
    giaTrungThauDaDieuChinh = df.iloc[:, 13].tolist()
    donViTrungThau = df.iloc[:, 14].tolist()
    tenCongTy = df.iloc[:, 15].tolist()
    loThau = df.iloc[:, 16].tolist()
    soLuongTrungThau = df.iloc[:, 20].tolist()
    thanhTien = df.iloc[:, 21].tolist()

    # Thêm vào danh mục Hoạt chất
    def check_hoat_chat(hoat_chat):
        mycursor.execute('select hoatChat from hoatchat where hoatChat = %s', (hoat_chat,))
        results = mycursor.fetchall()
        if len(results) > 0:
            return True
        else:
            return False

    newHoatChat = [capitalize_words(x.strip()) for x in hoatChat]
    sortedHoatChat = sorted(set(newHoatChat))
    for hc in sortedHoatChat:
        if not check_hoat_chat(hc):
            mycursor.execute('insert into hoatchat(hoatChat) values (%s)', (hc,))

    # Thêm vào danh mục Thuốc, Thông tin thuốc
    def check_thuoc(ten_thuoc):
        mycursor.execute('select tenThuoc from thuoc where tenThuoc = %s', (ten_thuoc,))
        results = mycursor.fetchall()
        if len(results) > 0:
            return True
        else:
            return False

    newTenThuoc = [capitalize_words(x.strip()) for x in tenThuoc]
    sortedTenThuoc = sorted(newTenThuoc)
    for ten_thuoc in sortedTenThuoc:
        if not check_thuoc(ten_thuoc):
            index = newTenThuoc.index(ten_thuoc)
            hoat_chat = newHoatChat[index]
            ham_luong = hamLuong[index]
            duong_dung = duongDung[index]
            dang_bao_che = dangBaoChe[index]
            dang_trinh_bay = dangTrinhBay[index]
            don_vi_tinh = donviTinh[index]
            hang_SX = hangSX[index].strip()
            nuoc_SX = nuocSX[index].strip()
            so_DK = soDK[index]
            mycursor.execute('select idHoatChat from hoatchat where hoatChat = %s', (hoat_chat,))
            idHoatChat = mycursor.fetchall()[0][0]
            mycursor.execute('insert into thuoc(tenThuoc, idHoatChat) values (%s, %s)', (ten_thuoc, idHoatChat))
            idThuoc = mycursor.lastrowid
            mycursor.execute('''insert into thongtinthuoc(idThuoc, hamLuong, duongDung, dangBaoChe, dangTrinhBay, donViTinh,
                    hangSX, nuocSX, soDK) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                             (idThuoc, ham_luong, duong_dung, dang_bao_che, dang_trinh_bay, don_vi_tinh, hang_SX,
                              nuoc_SX,
                              so_DK))

    # Nhập kết quả trúng thầu
    def check_nan(x):
        import math
        if math.isnan(x):
            return 0
        else:
            return int(x)

    def check_ket_qua(ma_thau, idThuoc):
        mycursor.execute('select idKetQua from ketquatrungthau where maThau = %s and idThuoc = %s', (ma_thau, idThuoc))
        results = mycursor.fetchall()
        if len(results) > 0:
            return True
        else:
            return False

    for i in range(len(maThau)):
        mycursor.execute('select idThuoc from thuoc where tenThuoc = %s', (newTenThuoc[i],))
        idThuoc = mycursor.fetchall()[0][0]
        if not check_ket_qua(maThau[i], idThuoc):
            lo_thau = capitalize_words(loThau[i].strip())
            date_format = '%d/%m/%Y'
            ngay_QD = datetime.strptime(ngayQD[i].strip(), date_format).date()
            ngay_het_han = datetime.strptime(ngayHetHan[i].strip(), date_format).date()
            gia_trung_thau = check_nan(giaTrungThau[i])
            gia_trung_thau_da_dieu_chinh = check_nan(giaTrungThauDaDieuChinh[i])
            so_luong_trung_thau = check_nan(soLuongTrungThau[i])
            thanh_tien = check_nan(thanhTien[i])

            mycursor.execute('''insert into ketquatrungthau(maThau, soQD, ngayQD, ngayHetHan, idThuoc, giaTrungThau, 
            giaTrungThauDaDieuChinh, donViTrungThau, tenCongTy, loThau, soLuongTrungThau, thanhTien) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                             (maThau[i], soQD[i], ngay_QD, ngay_het_han, idThuoc, gia_trung_thau,
                              gia_trung_thau_da_dieu_chinh, donViTrungThau[i], tenCongTy[i], lo_thau,
                              so_luong_trung_thau,
                              thanh_tien))

    mydb.commit()


def layDanhMucThuoc():
    mycursor.execute("select * from thuoc order by tenThuoc asc")
    results = mycursor.fetchall()
    danhMucThuoc = []
    for i in range(len(results)):
        newRow = []
        newRow.append(i + 1)
        newRow.append(results[i][1])

        idHoatChat = results[i][2]
        mycursor.execute("select hoatChat from hoatchat where idHoatChat = %s", (idHoatChat,))
        hoatChat = mycursor.fetchall()[0][0]
        newRow.append(hoatChat)
        danhMucThuoc.append(newRow)
    return danhMucThuoc


def layDanhMucHoatChat():
    mycursor.execute("select hoatChat from hoatchat order by hoatChat asc")
    results = mycursor.fetchall()
    danhMucHoatChat = []
    for i in range(len(results)):
        hoatChat = []
        hoatChat.append(i + 1)
        hoatChat.append(results[i][0])
        danhMucHoatChat.append(hoatChat)
    return danhMucHoatChat


def layDuongDan():
    mycursor.execute("select duongDan from duongdan")
    results = mycursor.fetchall()
    if len(results) > 0:
        return results[0][0]
    else:
        return ""


def nhapDuongDan(duongDan):
    mycursor.execute("truncate table duongdan")
    mycursor.execute("insert into duongdan(duongDan) values (%s)", (duongDan,))


def checkDuongDan(duongDan):
    khoChanPath = f'{duongDan}/Kho chẵn'
    khoLePath = f'{duongDan}/Kho lẻ'
    if not os.path.exists(khoChanPath):
        return "Không thấy thư mục Kho chẵn"
    elif not os.path.exists(khoLePath):
        return "Không tìm thấy thư mục Kho lẻ"
    else:
        return "Success"

def check_date_modified(path):
    name = os.path.basename(path)
    m_time = os.path.getmtime(path)
    dt_time = datetime.fromtimestamp(m_time).strftime('%Y-%m-%d %H:%M:%S')

    df = pd.read_excel(path)
    headers = df.columns.tolist()
    ten_thuoc = capitalize_words(headers[2].split(' : ')[1].strip())
    ma_thau = headers[4].split(' : ')[1].strip()
    mycursor.execute('select idThuoc from thuoc where tenThuoc = %s', (ten_thuoc,))
    idThuoc = mycursor.fetchall()[0][0]
    mycursor.execute('select idKetQua from ketquatrungthau where maThau = %s and idThuoc = %s', (ma_thau, idThuoc))
    idKetQua = mycursor.fetchall()[0][0]

    mycursor.execute('select idFile, ngayChinhSua from filekhochankhole where tenFile = %s', (name,))
    results = mycursor.fetchall()
    if len(results) == 0:
        mycursor.execute('insert into filekhochankhole (tenFile, ngayChinhSua, idKetQua) values (%s, %s, %s)',
                         (name, dt_time, idKetQua))
        mydb.commit()
        return True
    else:
        dt_time_db = results[0][1].strftime('%Y-%m-%d %H:%M:%S')
        fileID = results[0][0]
        if dt_time_db == dt_time:
            return False
        else:
            mycursor.execute('update filekhochankhole set ngayChinhSua = %s where idFile = %s', (dt_time, fileID))
            mydb.commit()
            return True

def nhapDuLieuKhoChan(duongDan):
    khoChanPath = f'{duongDan}/Kho chẵn'
    file_list = os.listdir(khoChanPath)
    for file in file_list:
        file_path = f'{khoChanPath}/{file}'
        if check_date_modified(file_path):
            name = os.path.basename(file_path)
            mycursor.execute('select idFile from filekhochankhole where tenFile = %s', (name,))
            idFile = mycursor.fetchall()[0][0]
            mycursor.execute('delete from khochan where idFile = %s', (idFile,))

            df = pd.read_excel(file_path)
            df = df.where(pd.notna(df), None)
            for i in range(2, df.shape[0] - 1):
                row = df.iloc[i].tolist()[:-2]
                ngay = row[0]
                nhap = int(row[4])
                ton = int(row[6])
                xuat = int(row[5])
                mycursor.execute("insert into khochan(idFile, ngay, nhap, xuat, ton) values (%s, %s, %s, %s, %s)",
                                 (idFile, ngay, nhap, xuat, ton))
    mydb.commit()


def nhapDuLieuKhoLe(duongDan):
    khoLePath = f'{duongDan}/Kho lẻ'
    file_list = os.listdir(khoLePath)
    for file in file_list:
        file_path = f'{khoLePath}/{file}'
        if check_date_modified(file_path):
            name = os.path.basename(file_path)
            mycursor.execute('select idFile from filekhochankhole where tenFile = %s', (name,))
            idFile = mycursor.fetchall()[0][0]
            mycursor.execute('delete from khochan where idFile = %s', (idFile,))

            df = pd.read_excel(file_path)
            df = df.where(pd.notna(df), None)
            for i in range(2, df.shape[0] - 1):
                row = df.iloc[i].tolist()[:-1]
                ngay = row[0]
                nhap = int(row[4])
                ton = int(row[6])
                xuat = int(row[5])
                mycursor.execute("insert into khole(idFile, ngay, nhap, xuat, ton) values (%s, %s, %s, %s, %s)",
                                 (idFile, ngay, nhap, xuat, ton))
    mydb.commit()


def mergeDuLieu():
    mycursor.execute('truncate table thongke')
    mycursor.execute('select distinct idFile from khochan')
    results = mycursor.fetchall()
    idFiles = [r[0] for r in results]
    for idFile in idFiles:
        mycursor.execute('select ngay, nhap from khochan where idFile = %s and nhap > 0', (idFile,))
        ngayNhapChans = mycursor.fetchall()

        mycursor.execute('select idKetQua from filekhochankhole where idFile = %s', (idFile,))
        idKetQua = mycursor.fetchall()[0][0]

        mycursor.execute('select idThuoc, soLuongTrungThau, loThau, maThau from ketquatrungthau where idKetQua = %s', (idKetQua,))
        idThuoc, soLuongTrungThau, loThau, maThau = mycursor.fetchall()[0]
        conlai = soLuongTrungThau

        mycursor.execute('select tenThuoc, idHoatChat from thuoc where idThuoc = %s', (idThuoc,))
        tenThuoc, idHoatChat = mycursor.fetchall()[0]

        mycursor.execute('select hoatChat from hoatchat where idHoatChat = %s', (idHoatChat,))
        hoatChat = mycursor.fetchall()[0][0]

        mycursor.execute('select idFile, tenFile from filekhochankhole where idKetQua = %s', (idKetQua,))
        results = mycursor.fetchall()
        for row in results:
            if 'kho lẻ' in row[1]:
                idFileLe = row[0]
                mycursor.execute('select ngay, ton, nhap from khole where idFile = %s', (idFileLe,))
                rs = mycursor.fetchall()
                rs_ngay = [r[0] for r in rs]
                sumNhapChan = 0
                nhapChanCungNgay = 0
                for i in range(len(ngayNhapChans)):
                    if i == 0:
                        tongdutru = soLuongTrungThau
                    else:
                        tongdutru = 0
                    ngay = ngayNhapChans[i][0]
                    nhapChan = ngayNhapChans[i][1]
                    nhapChanCungNgay += nhapChan
                    if i < len(ngayNhapChans) - 1:
                        if ngay == ngayNhapChans[i+1][0]:
                            continue
                        else:
                            nhapChan = nhapChanCungNgay
                            nhapChanCungNgay = 0
                    sumNhapChan += nhapChan
                    trungBinhNhapChan = round(sumNhapChan / (i+1), 0)
                    ngayNhapChan = ngay
                    if ngay <= rs_ngay[0]:
                        index = 0
                    elif ngay in rs_ngay:
                        index = rs_ngay.index(ngay) - 1
                    else:
                        while ngay not in rs_ngay:
                            ngay = ngay - timedelta(days=1)
                        index = None
                        for idx in range(len(rs_ngay) - 1, -1, -1):
                            if rs_ngay[idx] == ngay:
                                index = idx
                                break

                    closest_date = rs_ngay[index]
                    if index == 0:
                        tonle = rs[0][1] - rs[0][2]
                    else:
                        tonle = rs[index][1]

                    conlai -= nhapChan
                    mycursor.execute('''insert into thongke(ngaynhapchan, tenthuoc, hoatchat, lothau, mathau, nhapchan, tonle, 
                    dutruconlai, tongdutru, trungbinhnhapchan) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                     (ngayNhapChan, tenThuoc, hoatChat, loThau, maThau, nhapChan, tonle, conlai, tongdutru,
                                      trungBinhNhapChan))

        mydb.commit()

mergeDuLieu()
