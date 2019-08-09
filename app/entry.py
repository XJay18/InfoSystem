import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as dialog

import requests
import json
import csv
from InfoSystem.app.res.string import strings_cn as str_set
from InfoSystem.app.res.font import fonts_cn as fonts_set

window = tk.Tk()
window.title(str_set['win_title'])
window.geometry('800x400')

label = tk.Label(window,
                 text=str_set['win_title'],
                 font=(fonts_set['YaHeiB'], 20),
                 width=30, height=2)
label.pack(pady=10)

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
    relief='sunken').grid(row=0, column=1)

# query end time
tk.Label(mainFrame,
         text=str_set['time_end'],
         font=(fonts_set['YaHei'], 14),
         width=15, height=2).grid(row=1, column=0)
et_time_end = tk.Entry(
    mainFrame, bd='3',
    font=(fonts_set['YaHei'], 12),
    relief='sunken').grid(row=1, column=1)

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
                    values=(
                        dict_record.get('lec_title', str_set['default']),
                        dict_record.get('lecturer', str_set['default']),
                        dict_record.get('lec_time', str_set['default']),
                        dict_record.get('loc', str_set['default']),
                        dict_record.get('uni', str_set['default']),
                        dict_record.get('url', str_set['default']),
                        dict_record.get('issued_time', str_set['default'])))


def save_json(dict_info):
    fname = dialog.asksaveasfilename(initialfile=str_set['query_result'],
                                     defaultextension='.json')
    with open(fname, 'w')as f:
        json.dump(dict_info, f, ensure_ascii=False)
    return


def save_csv(dict_info):
    fname = dialog.asksaveasfilename(initialfile=str_set['query_result'],
                                     defaultextension='.csv')
    with open(fname, 'w')as f:
        fcsv = csv.DictWriter(f, dict_info[1])
        fcsv.writeheader()
        fcsv.writerows(dict_info[0])
    return


def inquery(event=None):
    window_inquery = tk.Toplevel(window)
    window_inquery.title(str_set['query_result'])
    inqueryMenu = tk.Menu(window_inquery)
    resultMenu = tk.Menu(inqueryMenu, tearoff=0)
    tree = ttk.Treeview(window_inquery, show='headings', height=20)
    tree["columns"] = (str_set['lec_title'],
                       str_set['lecturer'],
                       str_set['lec_time'],
                       str_set['loc'],
                       str_set['uni'],
                       str_set['url'],
                       str_set['issued_time'])
    tree.column(str_set['lec_title'], width=600)
    tree.column(str_set['lecturer'], width=80)
    tree.column(str_set['lec_time'], width=80)
    tree.column(str_set['loc'], width=100)
    tree.column(str_set['uni'], width=80)
    tree.column(str_set['issued_time'], width=80)
    tree.column(str_set['url'], width=400)

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

    print(data)

    # TODO: Time period condition

    resp = requests.post("http://localhost:5000/api/getInfo", data)
    dict_info = resp.json()['data']
    dict_keys = resp.json()['keys']

    dict_len = len(dict_info)
    for i in range(dict_len):
        insert_record(tree, i, dict_info[i])
    inqueryMenu.add_cascade(label=str_set['get'], menu=resultMenu)
    resultMenu.add_command(label=str_set['get_json'], command=lambda: save_json(dict_info))
    resultMenu.add_command(label=str_set['get_csv'], command=lambda: save_csv((dict_info, dict_keys)))
    tree.pack()
    window_inquery.config(menu=inqueryMenu)
    window_inquery.mainloop()


def about():
    window_about = tk.Toplevel(window)
    window_about.title(str_set['about'])
    about = tk.PhotoImage(file='./res/about.png')
    lb_about = tk.Label(window_about, image=about)
    lb_about.pack()
    window_about.mainloop()


bottomFrame = tk.Frame(window)
bottomFrame.pack()

# btn setting
tk.Button(bottomFrame,
          text=str_set['setting'],
          font=(fonts_set['YaHei'], 12),
          width=10).grid(row=0, column=0, padx=50)
# btn query
btn_query = tk.Button(bottomFrame,
                      text=str_set['query'],
                      font=(fonts_set['YaHeiB'], 12),
                      command=inquery,
                      width=10)

# hot key for query
btn_query.bind_all("q", inquery)
btn_query.bind_all("Q", inquery)
btn_query.grid(row=0, column=1, padx=50)

footFrame = tk.Frame(window)
footFrame.pack(side='bottom', pady=10)
# version
tk.Label(footFrame,
         text=str_set['version'] + str_set['curr_ver'],
         font=(fonts_set['YaHei'], 12),
         width=15, height=2).grid(row=0, column=0)
# about
tk.Button(footFrame,
          text=str_set['about'],
          font=(fonts_set['YaHei'], 12),
          command=about,
          width=10).grid(row=0, column=1)
window.mainloop()
