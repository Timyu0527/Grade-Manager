from tkinter import filedialog, ttk
import pandas as pd
import dataframe_image as dfi
import numpy as np
import os, copy 
import tkinter as tk

def selectInputFile():
    currdir = os.getcwd()
    target = filedialog.askopenfilename(parent=win, initialdir=currdir, title='Please select a directory')
    tkTarget = tk.StringVar()
    tkTarget.set(target)
    enInput.config(textvariable=tkTarget)

def selectOutputPath():
    currdir = os.getcwd()
    target = filedialog.askdirectory(parent=win, initialdir=currdir, title='Please select a directory')
    tkTarget = tk.StringVar()
    tkTarget.set(target)
    enOutput.config(textvariable=tkTarget)

def exportImage():
    with open(enInput.getvar(enInput.cget("textvariable")), newline='') as csvfile:
        df = pd.read_csv(csvfile)
        df = df.replace(np.nan, '', regex=True)
        df["總分"] = np.array([int(x) if x%1==0 else round(x,1) for x in df["總分"].values ], dtype=object)
        subdf = copy.deepcopy(df.iloc[0:5])
        for i in range(df.shape[0]):
            name = df.iloc[i]['姓名']
            subdf.loc[5] = copy.deepcopy(df.iloc[i])
            subdf.loc[5, '排名'] = '自己'
            df_styled = subdf.style.set_table_styles([dict(selector='th',
                                                    props=[('text-align', 'center'),
                                                            ('background-color', '#555555'),
                                                            ('color', 'white'),
                                                            ('font-size', '16px'),
                                                            ('border-bottom', '0px solid #555555')])])
            df_styled.set_properties(**{'font-size': '16px', 'height': '3em', 'border-bottom': '1px solid #999999'}).hide_index().render()
            pd.set_option('colheader_justify', 'center')
            pd.set_option("display.precision", 1)
            # print(enOutput.getvar(enOutput.cget("textvariable")))
            # df_styled.to_html('.\\test.html')
            dfi.export(df_styled, enOutput.getvar(enOutput.cget("textvariable")) + '/' + name + '.png')
        tkTarget = tk.StringVar()
        tkTarget.set('')
        enInput.config(textvariable=tkTarget)
        enOutput.config(textvariable=tkTarget)
    
if __name__ == '__main__':
    win = tk.Tk()
    win.title("Grade Manager")

    # win.geometry("800x600")

    win.tk.call('wm', 'iconphoto', win._w, tk.PhotoImage(file="grade.ico"))

    inputLabel = ttk.Label(win, text='請選擇檔案：')
    inputLabel.grid(row=0, column=0, padx=10, pady=10)

    enInput = tk.Entry(width=70)
    enInput.grid(row=0, column=1, padx=10, pady=10)

    btn = ttk.Button(text="瀏覽")
    btn.config(command=selectInputFile)
    btn.grid(row=0, column=2, padx=10, pady=10)

    outputLabel = ttk.Label(win, text='請選擇輸出路徑：')
    outputLabel.grid(row=1, column=0, padx=10, pady=10)

    enOutput = tk.Entry(width=70)
    enOutput.grid(row=1, column=1, padx=10, pady=10)

    btn2 = ttk.Button(text="瀏覽")
    btn2.config(command=selectOutputPath)
    btn2.grid(row=1, column=2, padx=10, pady=10)

    btn3 = ttk.Button(text="確定")
    btn3.config(command=exportImage)
    btn3.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    btnCancel = ttk.Button(text="取消", command=win.destroy)
    btnCancel.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    win.mainloop()


