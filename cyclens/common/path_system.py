# -*- coding: utf-8 -*-

import os


# Bütün sistemin işleyeceğini belirleyen yolur oluşturur
# Örnek: path: '/tmp/cyclens/face-regoctition'
def create_folder_root(path):
    try:
        os.makedirs(path)
        return True
    except OSError:
        print("Creation of the directory %s failed" % path)
    return False


# Path'ı verilen yere 'folder_id' isimli bir Folder oluşturur
def create_folder_id(path, folder_id):
    try:
        dir = '{}/{}'.format(path, folder_id)
        if not os.path.isdir(dir):
            os.mkdir(dir)
            return True
    except OSError:
        print("Creation of the directory %s failed" % path)
    return False


# Path bir Directory mi kontrol edilir
def check_folder_root(path):
    return os.path.isdir(path)


# Klasör adı (ID) en yüksek olanı döndürür
# '-1' döner <--- Hiç klasör yoksa
def get_latest_folder_id(path):
    highest = 0
    dirs = [entry.name for entry in os.scandir(os.path.abspath(path)) if entry.is_dir()]
    if len(dirs) == 0:
        return -1
    for folder in dirs:
        id = int(folder)
        if id >= highest:
            highest = id
    return highest


# Klasör adı (ID) içerisinde bulunan resimlerden, dosya adı en yüksek olanı döndürür,
# '-1' döner <--- Yol yoksa
def get_latest_face_id_from_folder_id(path, folder_id):
    highest = -1
    path_full = '{}/{}'.format(path, folder_id)
    walk = os.walk(os.path.abspath(path_full), topdown = False)

    for root, dirs, files in walk:
        for file in files:
            name, ext = os.path.splitext(file)
            id = int(name)
            if id >= highest:
                highest = id
        return highest
    return -1


# Kaç adet klasör var
# '0' döner <--- Eğer hiç klasör yoksa
def get_folder_count(path):
    dirs = [entry.name for entry in os.scandir(os.path.abspath(path)) if entry.is_dir()]
    return len(dirs)
