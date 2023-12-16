
import pymysql
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.scrolledtext import ScrolledText

# 建立数据库连接
def connect_database():
    host = entry_host.get()
    user = entry_user.get()
    password = entry_password.get()
    port = int(entry_port.get()) if entry_port.get() else 3306  # 获取端口号并转换为整数，默认为3306

    try:
        # 建立数据库连接
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

        # 保存连接对象
        global conn
        conn = connection

        # 获取数据库列表
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()

        # 清空数据库列表
        listbox_databases.delete(0, tk.END)

        # 在列表中显示数据库
        for database in databases:
            listbox_databases.insert(tk.END, database[0])

        # 关闭游标
        cursor.close()

        show_execution_page()

    except pymysql.Error as error:
        messagebox.showerror("连接错误", str(error))


# 修改数据源
def modify_data_source():
    # 隐藏执行界面
    frame_execution.pack_forget()

    # 显示连接界面
    frame_connect.pack()


# 设置数据源
def set_data_source():
    global conn

    # 关闭已有连接
    if conn:
        conn.close()
        conn = None

    # 清空连接信息
    entry_host.delete(0, tk.END)
    entry_port.delete(0, tk.END)
    entry_user.delete(0, tk.END)
    entry_password.delete(0, tk.END)

    # 显示连接界面
    frame_connect.pack()


# 执行SQL查询
def execute_sql():
    try:
        # 创建游标对象
        cursor = conn.cursor()

        # 执行SQL语句
        sql_statement = entry_sql.get()
        cursor.execute(sql_statement)

        # 获取结果（如果有）
        result = cursor.fetchall()

        # 清空文本框内容
        text_result.delete("1.0", tk.END)

        if result:
            # 在文本框中显示结果
            for row in result:
                row_str = ' '.join(str(col) for col in row)  # 将结果转换为字符串并删除分隔符
                text_result.insert(tk.END, row_str + "\n")

        # 关闭游标
        cursor.close()

    except pymysql.Error as error:
        messagebox.showerror("执行错误", str(error))


# 导出结果到文件
def export_result():
    result_text = text_result.get("1.0", tk.END)

    file_path = asksaveasfile(mode='w', defaultextension=".txt")
    if file_path:
        file_path.write(result_text)
        file_path.close()

        messagebox.showinfo("导出完成", "执行结果已导出到文件！")


# 显示执行界面
def show_execution_page():
    # 隐藏连接界面
    frame_connect.pack_forget()

    # 显示执行界面
    frame_execution.pack()


# 创建连接对象
conn = None

# 创建连接界面
window = tk.Tk()
window.title("MySQL连接与执行SQL语句")
window.geometry("600x400")

# 连接界面
frame_connect = tk.Frame(window)

# 连接配置面板
config_frame = tk.Frame(frame_connect, padx=10)
config_frame.pack(side=tk.LEFT)

# 主机
label_host = tk.Label(config_frame, text="主机:")
label_host.grid(row=0, column=0, sticky="w")
entry_host = tk.Entry(config_frame)
entry_host.grid(row=0, column=1)

# 端口
label_port = tk.Label(config_frame, text="端口:")
label_port.grid(row=1, column=0, sticky="w")
entry_port = tk.Entry(config_frame)
entry_port.insert(tk.END, "3306")  # 默认端口为3306
entry_port.grid(row=1, column=1)

# 用户名
label_user = tk.Label(config_frame, text="用户名:")
label_user.grid(row=2, column=0, sticky="w")
entry_user = tk.Entry(config_frame)
entry_user.grid(row=2, column=1)

# 密码
label_password = tk.Label(config_frame, text="密码:")
label_password.grid(row=3, column=0, sticky="w")
entry_password = tk.Entry(config_frame)
entry_password.grid(row=3, column=1)

# 连接按钮
button_connect = tk.Button(config_frame, text="连接", command=connect_database)
button_connect.grid(row=4, column=0, columnspan=2, pady=10)

# 数据库列表
label_databases = tk.Label(frame_connect, text="数据库列表:")
label_databases.pack(anchor="w")
listbox_databases = tk.Listbox(frame_connect, width=30, height=10)
listbox_databases.pack(anchor="w")

# 执行界面
frame_execution = tk.Frame(window)

# SQL输入框
label_sql = tk.Label(frame_execution, text="输入SQL语句:")
label_sql.pack(anchor="w")
entry_sql = tk.Entry(frame_execution, width=50)
entry_sql.pack(anchor="w")

# 执行按钮
button_execute = tk.Button(frame_execution, text="执行", command=execute_sql)
button_execute.pack(anchor="w", pady=10)

# 结果文本框
label_result = tk.Label(frame_execution, text="执行结果:")
label_result.pack(anchor="w")
text_result = ScrolledText(frame_execution, width=60, height=10)
text_result.pack(anchor="w")

# 导出按钮
button_export = tk.Button(frame_execution, text="导出结果", command=export_result)
button_export.pack(anchor="w", pady=10)

# 菜单栏
menubar = tk.Menu(window)
window.config(menu=menubar)

# 文件菜单
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="设置数据源", command=set_data_source)
file_menu.add_command(label="修改数据源", command=modify_data_source)
file_menu.add_separator()
file_menu.add_command(label="退出", command=window.quit)

# 显示连接界面
show_execution_page()

# 启动主事件循环
window.mainloop()
