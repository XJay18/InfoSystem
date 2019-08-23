import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as dialog

import requests
import json
import csv
from app.res.string import strings_cn as str_set
from app.res.font import fonts_cn as fonts_set

window = tk.Tk()
window.title(str_set['win_title'])
window.geometry('800x420')

# Hyper Settings
style_btn = ttk.Style()
style_btn.configure('TButton',
                    font=(fonts_set['YaHei'], 10),
                    width=10)
label = tk.Label(window,
                 text=str_set['win_title'],
                 font=(fonts_set['YaHeiB'], 20),
                 width=30, height=2)
label.pack()


def save_json(dict_info):
    fname = dialog.asksaveasfilename(initialfile=str_set['query_result'],
                                     defaultextension='.json')
    with open(fname, 'w', encoding='gb18030')as f:
        json.dump(dict_info, f, ensure_ascii=False)
    return


def save_csv(dict_info):
    fname = dialog.asksaveasfilename(initialfile=str_set['query_result'],
                                     defaultextension='.csv')
    with open(fname, 'w', encoding='gb18030')as f:
        fcsv = csv.DictWriter(f, dict_info[1])
        fcsv.writeheader()
        fcsv.writerows(dict_info[0])
    return


def default_query(event=None):
    window_inquery = tk.Toplevel(window)
    inqueryMenu = tk.Menu(window_inquery)
    resultMenu = tk.Menu(inqueryMenu, tearoff=0)
    details_keys = [str_set['lec_title'],
                    str_set['lecturer'],
                    str_set['lec_time'],
                    str_set['loc'],
                    str_set['uni'],
                    str_set['url'],
                    str_set['issued_time']]
    tree = ttk.Treeview(window_inquery, show='headings', height=20)

    def look_detailed(event):
        window_detailed = tk.Toplevel(window_inquery)
        window_detailed.title(str_set['detailed'])
        curItem = tree.selection()
        details = tree.item(curItem).get('values', None)

        if details:
            for idx in range(7):
                tk.Label(window_detailed,
                         text=details_keys[idx],
                         font=(fonts_set['YaHei'], 10),
                         width=15, height=2).grid(row=idx, column=0)
                text = ttk.Entry(window_detailed, width=100)
                text.insert('end', details[idx])
                text.config(state='readonly')
                text.grid(row=idx, column=1)
                tk.Label(window_detailed,
                         text=' ' * 10,
                         width=10).grid(row=idx, column=2)

    # double click an item to see detailed
    tree.bind('<Double-Button-1>', look_detailed)
    tree["columns"] = tuple(details_keys)
    tree.column(str_set['lec_title'], width=600)
    tree.column(str_set['lecturer'], width=160)
    tree.column(str_set['lec_time'], width=200)
    tree.column(str_set['loc'], width=160)
    tree.column(str_set['uni'], width=80)
    tree.column(str_set['issued_time'], width=80)
    tree.column(str_set['url'], width=200)

    tree.heading(str_set['lec_title'], text=str_set['lec_title'])
    tree.heading(str_set['lecturer'], text=str_set['lecturer'])
    tree.heading(str_set['lec_time'], text=str_set['lec_time'])
    tree.heading(str_set['loc'], text=str_set['loc'])
    tree.heading(str_set['uni'], text=str_set['uni'])
    tree.heading(str_set['issued_time'], text=str_set['issued_time'])
    tree.heading(str_set['url'], text=str_set['url'])
    resp = requests.get("http://localhost:5000/api/getInfo")
    dict_info = resp.json()['data']
    dict_keys = resp.json()['keys']

    dict_len = len(dict_info)
    window_inquery.title(str_set['query_result'] + str_set['compute_1'] + str(dict_len) + str_set['compute_2'])
    for i in range(dict_len):
        insert_record(tree, i, dict_info[i])
    inqueryMenu.add_cascade(label=str_set['get'], menu=resultMenu)
    resultMenu.add_command(label=str_set['get_json'], command=lambda: save_json(dict_info))
    resultMenu.add_command(label=str_set['get_csv'], command=lambda: save_csv((dict_info, dict_keys)))
    tree.pack()
    window_inquery.config(menu=inqueryMenu)
    window_inquery.mainloop()


# btn default query
btn_default_query = ttk.Button(window,
                               text=str_set['default_query'],
                               command=default_query,
                               style='TButton')

# hot key for default query
btn_default_query.bind_all("<Shift-D>", default_query)
btn_default_query.pack()
tk.Label(window, text=' - ' * 50).pack()

mainFrame = tk.Frame(window)
mainFrame.pack()

# query start time
tk.Label(mainFrame,
         text=str_set['time_start'],
         font=(fonts_set['YaHei'], 14),
         width=15, height=2).grid(row=0, column=0)
et_time_start = tk.Entry(
    mainFrame, bd='3',
    font=(fonts_set['YaHei'], 12),
    relief='sunken')
et_time_start.grid(row=0, column=1)

# query end time
tk.Label(mainFrame,
         text=str_set['time_end'],
         font=(fonts_set['YaHei'], 14),
         width=15, height=2).grid(row=1, column=0)
et_time_end = tk.Entry(
    mainFrame, bd='3',
    font=(fonts_set['YaHei'], 12),
    relief='sunken')
et_time_end.grid(row=1, column=1)

# query uni
tk.Label(mainFrame,
         text=str_set['uni'],
         font=(fonts_set['YaHei'], 14),
         width=15, height=2).grid(row=2, column=0)
et_uni = tk.Entry(
    mainFrame, bd='3',
    font=(fonts_set['YaHei'], 12),
    relief='sunken')
et_uni.grid(row=2, column=1)

# query keywords
tk.Label(mainFrame,
         text=str_set['klist'],
         font=(fonts_set['YaHei'], 12),
         width=15, height=2).grid(row=0, column=3, columnspan=2)
klistFrame = tk.Frame(mainFrame)
klistFrame.grid(row=1, rowspan=2, column=3, columnspan=2, padx=10)
et_keyword = []
for c in range(2):
    for r in range(3):
        et = tk.Entry(klistFrame,
                      font=(fonts_set['YaHei'], 12),
                      width=20)
        et_keyword.append(et)
        et.grid(row=r, column=c, padx=5, pady=2)


# utils interface
def insert_record(treeview, index, dict_record):
    treeview.insert("", index,
                    values=(dict_record['lec_title'] if dict_record['lec_title'] is not "" else str_set['default'],
                            dict_record['lecturer'] if dict_record['lecturer'] is not "" else str_set['default'],
                            dict_record['lec_time'] if dict_record['lec_time'] is not "" else str_set['default'],
                            dict_record['loc'] if dict_record['loc'] is not "" else str_set['default'],
                            dict_record['uni'] if dict_record['uni'] is not "" else str_set['default'],
                            dict_record['url'] if dict_record['url'] is not "" else str_set['default'],
                            dict_record['issued_time'] if dict_record['issued_time'] is not "" else str_set['default']))


def inquery(event=None):
    window_inquery = tk.Toplevel(window)
    inqueryMenu = tk.Menu(window_inquery)
    resultMenu = tk.Menu(inqueryMenu, tearoff=0)
    details_keys = [str_set['lec_title'],
                    str_set['lecturer'],
                    str_set['lec_time'],
                    str_set['loc'],
                    str_set['uni'],
                    str_set['url'],
                    str_set['issued_time']]
    tree = ttk.Treeview(window_inquery, show='headings', height=20)

    def look_detailed(event):
        window_detailed = tk.Toplevel(window_inquery)
        window_detailed.title(str_set['detailed'])
        curItem = tree.selection()
        details = tree.item(curItem).get('values', None)

        if details:
            for idx in range(7):
                tk.Label(window_detailed,
                         text=details_keys[idx],
                         font=(fonts_set['YaHei'], 10),
                         width=15, height=2).grid(row=idx, column=0)
                text = ttk.Entry(window_detailed, width=100)
                text.insert('end', details[idx])
                text.config(state='readonly')
                text.grid(row=idx, column=1)
                tk.Label(window_detailed,
                         text=' ' * 10,
                         width=10).grid(row=idx, column=2)

    # double click an item to see detailed
    tree.bind('<Double-Button-1>', look_detailed)
    tree["columns"] = tuple(details_keys)
    tree.column(str_set['lec_title'], width=600)
    tree.column(str_set['lecturer'], width=160)
    tree.column(str_set['lec_time'], width=200)
    tree.column(str_set['loc'], width=160)
    tree.column(str_set['uni'], width=80)
    tree.column(str_set['issued_time'], width=80)
    tree.column(str_set['url'], width=200)

    tree.heading(str_set['lec_title'], text=str_set['lec_title'])
    tree.heading(str_set['lecturer'], text=str_set['lecturer'])
    tree.heading(str_set['lec_time'], text=str_set['lec_time'])
    tree.heading(str_set['loc'], text=str_set['loc'])
    tree.heading(str_set['uni'], text=str_set['uni'])
    tree.heading(str_set['issued_time'], text=str_set['issued_time'])
    tree.heading(str_set['url'], text=str_set['url'])

    # keywords condition
    keywords = ""
    for k in et_keyword:
        keywords += str(k.get()).strip() + '|'
    data = {'keywords': keywords}

    # uni condition
    if et_uni.get() is not None and et_uni.get() != "":
        uni = str(et_uni.get())
        data.update({"uni": uni})

    # Time period condition
    if et_time_start.get() is not None and et_time_start.get() != "":
        time_start = str(et_time_start.get())
        data.update({"time_start": time_start})

    if et_time_end.get() is not None and et_time_end.get() != "":
        time_end = str(et_time_end.get())
        data.update({"time_end": time_end})

    resp = requests.post("http://localhost:5000/api/getInfo", data)
    dict_info = resp.json()['data']
    dict_keys = resp.json()['keys']

    dict_len = len(dict_info)
    window_inquery.title(str_set['query_result'] + str_set['compute_1'] + str(dict_len) + str_set['compute_2'])
    for i in range(dict_len):
        insert_record(tree, i, dict_info[i])
    inqueryMenu.add_cascade(label=str_set['get'], menu=resultMenu)
    resultMenu.add_command(label=str_set['get_json'], command=lambda: save_json(dict_info))
    resultMenu.add_command(label=str_set['get_csv'], command=lambda: save_csv((dict_info, dict_keys)))
    tree.pack()
    window_inquery.config(menu=inqueryMenu)
    window_inquery.mainloop()


def setting(event=None):
    window_setting = tk.Toplevel(window)
    window_setting.title(str_set['setting'])
    sort_type = tk.StringVar()

    # get set value
    resp = requests.get("http://localhost:5000/api/getSettings")
    sort_type.set(resp.json().get('sort_type', 'lec_time'))

    # sort type
    tk.Label(window_setting,
             text=str_set['sort_type'],
             font=(fonts_set['YaHei'], 10),
             width=10, height=2).grid(row=0, column=0)
    rd_sort_type_issue = ttk.Radiobutton(window_setting, text='按发布时间', value='issued_time', variable=sort_type)
    rd_sort_type_lecture = ttk.Radiobutton(window_setting, text='按举办时间', value='lec_time', variable=sort_type)

    rd_sort_type_issue.grid(row=0, column=1, padx=5)
    rd_sort_type_lecture.grid(row=0, column=2, padx=5)
    tk.Label(window_setting,
             text=' ' * 5,
             width=2).grid(row=0, column=3)

    def setting_done(event=None):
        params = {'sort_type': sort_type.get()}
        requests.post("http://localhost:5000/api/setSettings", params)
        window_setting.destroy()

    btn_set_done = ttk.Button(window_setting,
                              style='TButton',
                              text=str_set['confirm'],
                              command=setting_done)
    btn_set_done.grid(row=1, column=0, columnspan=4)
    tk.Label(window_setting,
             text=' ' * 10,
             width=5).grid(row=2)


def about():
    window_about = tk.Toplevel(window)
    window_about.title(str_set['about'])
    about = tk.PhotoImage(file='./res/about.png')
    lb_about = tk.Label(window_about, image=about)
    lb_about.pack()
    window_about.mainloop()


def add_web():
    window_addweb = tk.Toplevel(window)
    window_addweb.title(str_set['add_web'])
    tk.Label(window_addweb,
             text=str_set['add_web'],
             font=(fonts_set['YaHei'], 10),
             width=10, height=2).grid(row=0, column=0)
    et_website = ttk.Entry(window_addweb, width=100)
    et_website.grid(row=0, column=1)
    tk.Label(window_addweb,
             text=' ' * 5,
             width=2).grid(row=0, column=2)

    def send_addweb(event=None):
        requests.post("http://localhost:5000/api/appendWeb",
                      {'website': str(et_website.get()).strip()})
        window_addweb.destroy()

    ttk.Button(window_addweb,
               text=str_set['add_web_confirm'],
               style='TButton',
               command=send_addweb).grid(row=1, column=0, columnspan=3)
    tk.Label(window_addweb,
             text=' ' * 10,
             width=5).grid(row=2)
    window_addweb.mainloop()


bottomFrame = tk.Frame(window)
bottomFrame.pack()

# btn setting
btn_setting = ttk.Button(bottomFrame,
                         text=str_set['setting'],
                         command=setting,
                         style='TButton')

# hot key for setting
btn_setting.bind_all("<Shift-S>", setting)
btn_setting.grid(row=0, column=0, padx=50)

# btn query
btn_query = ttk.Button(bottomFrame,
                       text=str_set['query'],
                       command=inquery,
                       style='TButton')

# hot key for query
btn_query.bind_all("<Shift-Q>", inquery)
btn_query.grid(row=0, column=1, padx=50)

footFrame = tk.Frame(window)
footFrame.pack(side='bottom', pady=10)
# version
tk.Label(footFrame,
         text=str_set['version'] + str_set['curr_ver'],
         font=(fonts_set['YaHei'], 12),
         width=15, height=2).grid(row=0, column=0)

# add web
btn_addweb = ttk.Button(footFrame,
                        text=str_set['add_web'],
                        command=add_web,
                        style='TButton')
btn_addweb.grid(row=0, column=1, padx=10)

# about
ttk.Button(footFrame,
           text=str_set['about'],
           command=about,
           style='TButton').grid(row=0, column=2, padx=10)

window.mainloop()
