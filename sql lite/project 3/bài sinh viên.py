from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

from zmq.backend import first

root = Tk()
root.title("Hệ thống quản lý sinh viên ")
root.geometry("600x800")

# Kết nối tới db
# conn = sqlite3.connect('address_book.db')
# c = conn.cursor()
#
# # Tao bang de luu tru
c.execute(
    CREATE TABLE addresses(
        ma_sinh_vien  INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name text,
        last_name text,
        ma_lop text,
        năm_nhập_học  text,
        điểm_trung_bình  text,
    )



def them():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    # Lấy dữ liệu đã nhập
    first =f_name.get()
    lastName_value = l_name.get()
    masinhvien_value = masinhvien.get()
    namnhaphoc_value = namnhaphoc.get()
    diemtrungbinh_value = diemtrungbinh.get()
    malop_value = malop.get()
    # Thực hiện câu lệnh để thêm
    c.execute('''
        INSERT INTO 
        sinhvien (first_name, last_name, masinhvien, malop, namnhaphoc, diemtrungbinh)
        VALUES 
        (:name, :last_name, :masinhvien,:malop, :namnhaphoc, :diemtrungbinh)
    ''',{
        'name' : name_value,
        'last_name' : lastName_value,
        'masinhvien': masinhvien_value,
        'malop': malop_value,
        'namnhaphoc': namnhaphoc_value,
        'diemtrungbinh': diemtrungbinh_value,
      }
    )
    conn.commit()
    conn.close()

    # Reset form
    f_name.delete(0, END)
    l_name.delete(0, END)
    masinhvien_value.delete(0, END)
    malop_value.delete(0, END)
    namnhaphoc_value.delete(0, END)
    diemtrungbinh_value.delete(0, END)

    # Hien thi lai du lieu
    truy_van()

def xoa():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    c.execute('''DELETE FROM
                        sinhvien 
                      WHERE id=:id''',
              {'id':delete_box.get()})
    delete_box.delete(0, END)
    conn.commit()
    conn.close()
    # Hiên thi thong bao
    messagebox.showinfo("Thông báo", "Đã xóa!")
    # Hiển thị lại dữ liệu
    truy_van()


def truy_van():
    # Xóa đi các dữ liệu trong TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('sinhvien.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sinhvien")
    records = c.fetchall()

    # Hien thi du lieu
    for r in records:
        tree.insert("", END, values=(r[0], r[1], r[2]))

    # Ngat ket noi
    conn.close()
def chinh_sua():
    global editor
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("400x300")

    conn = sqlite3.connect('sinhvien.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id':record_id})
    records = c.fetchall()

    global f_id_editor, f_name_editor, l_name_editor, masinhvien_editor, malop_editor, namnhaphoc_editor, diemtrungbinh_editor

    f_masinhvien_editor = Entry(editor, width=30)
    f_masinhvien_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=1, column=1, padx=20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=2, column=1)
    f_malop_editor = Entry(editor, width=30)
    f_malop_editor.grid(row=3, column=1)
    f_namnhaphoc_editor = Entry(editor, width=30)
    f_namnhaphoc_editor.grid(row=4, column=1)
    f_diemtrungbinh_editor = Entry(editor, width=30)
    f_diemtrungbinh_editor.grid(row=5, column=1)


    f_masinhvien_label = Label(editor, text="Mã sinh viên")
    f_masinhvien_label.grid(row=0, column=0, pady=(10, 0))
    f_name_label = Label(editor, text="Họ")
    f_name_label.grid(row=1, column=0)
    l_name_editor = Label(editor, text="Tên")
    l_name_editor.grid(row=2, column=0)
    malop_label = Label(editor, text="Mã lớp")
    malop_label.grid(row=3, column=0)
    namnhaphoc_label = Label(editor, text="Năm nhập học")
    namnhaphoc_label.grid(row=4, column=0)
    diemtrungbinh_label = Label(editor, text="Điểm trung bình")
    diemtrungbinh_label.grid(row=5, column=0)


    for record in records:
        f_masinhvien_editor.insert(0, record[0])
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        f_malop_editor.insert(0, record[3])
        f_namnhaphoc_editor.insert(0, record[4])
        f_diemtrungbinh_editor.insert(0, record[5])


    edit_btn = Button(editor, text="Lưu bản ghi", command=cap_nhat)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

    def cap_nhat():
        conn = sqlite3.connect('address_book.db')
        c = conn.cursor()
        record_id = f_masinhvien_editor.get()

        c.execute("""UPDATE addresses SET
               first_name = :first,
               last_name = :last,
              masinhvien = :masinhvien,
               malop = :city,
               namnhaphoc = :state,
               diemtrungbinh = :zipcode
               WHERE id = :id""",
                  {
                      'first': f_name_editor.get(),
                      'last': l_name_editor.get(),
                      'malop': f_malop_editor.get(),
                      'namnhaphoc': f_namnhaphoc_editor.get(),
                      'diemtrungbinh': f_diemtrungbinh_editor.get(),

                      'id': record_id
                  })

        conn.commit()
        conn.close()
        editor.destroy()

        # Cập nhật lại danh sách bản ghi sau khi chỉnh sửa
        truy_van()

    # Khung cho các ô nhập liệu
    input_frame = Frame(root)
    input_frame.pack(pady=10)

    # Các ô nhập liệu cho cửa sổ chính
    f_name = Entry(input_frame, width=30)
    f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_ten = Entry(input_frame, width=30)
    l_ten.grid(row=1, column=1)
    f_malop = Entry(input_frame, width=30)
    f_malop.grid(row=2, column=1)
    f_namnhaphoc = Entry(input_frame, width=30)
    f_namnhaphoc.grid(row=3, column=1)
    f_diemtrungbinh = Entry(input_frame, width=30)
    f_diemtrungbinh.grid(row=4, column=1)
    zipcode = Entry(input_frame, width=30)
    zipcode.grid(row=5, column=1)

    # Các nhãn
    f_name_label = Label(input_frame, text="Họ")
    f_name_label.grid(row=0, column=0, pady=(10, 0))
    l_ten_label = Label(input_frame, text="Tên")
    l_ten_label.grid(row=1, column=0)
    malop_label = Label(input_frame, text="Mã lớp")
    malop_label.grid(row=2, column=0)
    namnhaphoc_label = Label(input_frame, text="Năm nhập học")
    namnhaphoc_label.grid(row=3, column=0)
    diemtrungbinh_label = Label(input_frame, text="Điểm trung bình")
    diemtrungbinh_label.grid(row=4, column=0)


    # Khung cho các nút chức năng
    button_frame = Frame(root)
    button_frame.pack(pady=10)

    # Các nút chức năng
    submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
    submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
    query_btn = Button(button_frame, text="Hiển thị bản ghi", command=truy_van)
    query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
    delete_box_label = Label(button_frame, text="Chọn Mã sinh viên")
    delete_box_label.grid(row=2, column=0, pady=5)
    delete_box = Entry(button_frame, width=30)
    delete_box.grid(row=2, column=1, pady=5)
    delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
    delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
    edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
    edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

    # Khung cho Treeview
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    # Treeview để hiển thị bản ghi
    columns = ("Mã sinh viên", "Họ", "Tên")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    for column in columns:
        tree.column(column, anchor=CENTER)  # This will center text in rows
        tree.heading(column, text=column)
    tree.pack()

    # Gọi hàm truy vấn để hiển thị bản ghi khi khởi động


    root.mainloop()
