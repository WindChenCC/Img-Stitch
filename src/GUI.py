# -*- coding: utf-8 -*-
# !/usr/bin/env python
from panoramic_stitch import *
from simple_stitch import *

import os
import time
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
import cv2
import numpy as np


class GUIWindow:
    def __init__(self):

        self.win = Tk()
        self.win.iconbitmap(default=r'../res/icon.ico')
        self.win.title('Img Stitch')
        self.win.geometry('491x260')
        self.win.resizable(width=False, height=False)
        font = ('Microsoft YaHei', 10)
        self.image_names = []
        self.image_arrays = []
        self.image_types = []
        self.image_size = []
        self.image_time = []
        self.image_path = []
        self.save_dir = './output'

        self.ctrl = Frame(self.win)
        self.ctrl.grid(row=3, column=1, sticky=W)
        self.select_btn = Button(self.ctrl, text=_(u'选择图片'), width=7, font=font, command=self.select_image)
        self.horizon_btn = Button(self.ctrl, text=_(u'水平拼接'), width=7, font=font, command=self.horizon_stitch)
        self.vertical_btn = Button(self.ctrl, text=_(u'垂直拼接'), width=7, font=font, command=self.vertical_stitch)
        self.whole_stitch_btn = Button(self.ctrl, text=_(u'全景拼接(带黑边)'), width=13, font=font, command=self.whole_stitch)
        self.whole_stitch_crop_btn = Button(self.ctrl, text=_(u'全景拼接(去黑边)'), width=13, font=font,
                                            command=self.whole_stitch_crop)
        self.clear_btn = Button(self.ctrl, text=_(u'清空图片'), width=7, font=font, command=self.clear_image)

        self.func_btn_two = [self.horizon_btn, self.vertical_btn, self.whole_stitch_btn, self.whole_stitch_crop_btn]

        # disable button
        for btn in self.func_btn_two:
            btn.config(state='disabled')

        # init file info table
        self.ftree = ttk.Treeview(self.win, show='headings')
        self.ftree['columns'] = ('findex', 'fname', 'fdate', 'ftype', 'fsize')
        self.ftree.column('findex', width=26)
        self.ftree.column('fname', width=165)
        self.ftree.column('fdate', width=150)
        self.ftree.column('ftype', width=50)
        self.ftree.column('fsize', width=100)
        self.ftree.heading('fname', text=_(u'文件名'), anchor='w')
        self.ftree.heading('fdate', text=_(u'修改日期'), anchor='w')
        self.ftree.heading('ftype', text=_(u'类型'), anchor='w')
        self.ftree.heading('fsize', text=_(u'分辨率'), anchor='w')

        # grid layout
        self.select_btn.grid(row=1, column=1, sticky=W)
        self.horizon_btn.grid(row=1, column=2, sticky=W)
        self.vertical_btn.grid(row=1, column=3, sticky=W)
        self.whole_stitch_btn.grid(row=1, column=4, sticky=W)
        self.whole_stitch_crop_btn.grid(row=1, column=5, sticky=W)
        self.clear_btn.grid(row=1, column=6, sticky=W)
        self.ftree.grid(row=4, column=1, columnspan=3)

    def show(self):
        self.ftree.bind('<Double-1>', self.tree_double)
        self.win.mainloop()

    def select_image(self):
        img_paths = filedialog.askopenfilenames(title="Select PDF file",
                                                filetypes=[("image", ".jpeg"), ("image", ".png"), ("image", ".jpg"), ],
                                                initialdir=os.getcwd())

        for img_path in img_paths:
            img_name = img_path.split('/')[-1]
            self.image_path.append(img_path)
            self.image_names.append(img_name.split('.')[0])
            self.image_types.append(img_name.split('.')[-1])

            img_array = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
            self.image_arrays.append(img_array)
            self.image_size.append(img_array.shape)
            t_stamp = os.path.getmtime(img_path)
            t_array = time.localtime(t_stamp)
            t_date = time.strftime('%Y-%m-%d %H:%M:%S', t_array)
            self.image_time.append(t_date)

        # clear file tree
        self.clear_tree()
        for i in range(len(self.image_names)):
            img_size = str(self.image_size[i][1]) + '*' + str(self.image_size[i][0])
            self.ftree.insert('', i, text='',
                              values=(i + 1, self.image_names[i], self.image_time[i], self.image_types[i], img_size))

        # enable button when pictures > 1
        if len(self.image_arrays) >= 2:
            for btn in self.func_btn_two:
                btn.config(state='active')

    def vertical_stitch(self):
        img = vertical_stitch(self.image_arrays, self.save_dir)
        img_path = os.path.join(self.save_dir, 'vertical_stitched.jpg')
        if img is not None and os.path.exists(img_path):
            os.system('start ' + img_path)

    def horizon_stitch(self):
        img = horizon_stitch(self.image_arrays, self.save_dir)
        img_path = os.path.join(self.save_dir, 'horizon_stitched.jpg')
        if img is not None and os.path.exists(img_path):
            os.system('start ' + img_path)

    def whole_stitch(self):
        img = stitch(self.image_arrays, self.save_dir)
        img_path = os.path.join(self.save_dir, 'whole_stitched.jpg')
        if img is not None and os.path.exists(img_path):
            os.system('start ' + img_path)
        else:
            messagebox.showwarning('ERROR', 'failed')

    def whole_stitch_crop(self):
        img = stitch_crop(self.image_arrays, self.save_dir)
        img_path = os.path.join(self.save_dir, 'whole_stitched_crop.jpg')
        if img is not None and os.path.exists(img_path):
            os.system('start ' + img_path)
        else:
            messagebox.showwarning('ERROR', 'failed')

    def clear_image(self):
        self.clear_tree()
        self.image_names = []
        self.image_arrays = []
        self.image_types = []
        self.image_size = []
        self.image_time = []
        self.image_path = []

        # disable button
        for btn in self.func_btn_two:
            btn.config(state='disabled')

    def clear_tree(self):
        """
        clear Treeview
        """
        for item in self.ftree.get_children():
            self.ftree.delete(item)

    def tree_double(self):
        """
        double click event
        """
        for item in self.ftree.selection():
            item_text = self.ftree.item(item, "values")
            index = int(item_text[0]) - 1
            cv2.imshow(item_text[1], self.image_arrays[index])
