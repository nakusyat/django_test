# -*- coding: utf-8 -*-
import os


def move_temp_file(f, path):
    destination = open(path + f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def get_uploaded_files_by_extension(extensions, path):
    uploaded_files = os.listdir(path)
    files = []
    for item in uploaded_files:
        if item.endswith(tuple(extensions)):
            files.append(item)
    return files


def process_files(files, source_path, destination_path):
    for item in files:
        destination = open(destination_path + 'tok_' + item, 'wb+')
        special_words = ['ж.б.', 'о.э.']
        special_char = [',', '.', ':', ';', '(', ')', '!', '-', '"', '+', '%', u'\u201c', u'\u201d']
        with open(source_path + item, 'r') as fileinput:
            for line in fileinput:
                words = line.split(' ')
                words = filter(None, words)
                for word in words:
                    if word not in special_words:
                        word = word.decode('utf-8')
                        for ch in special_char:
                            if ch in word:
                                word = word.replace(ch, ' ')
                        word = word.lower().encode('utf-8')
                    if '\n' not in word:
                        word += ' '

                    word = ''.join([i for i in word if not i.isdigit()])

                    destination.write(word)
            destination.close()


def move_files_in_extensions(extensions, source_path, destination_path):
    source_files = os.listdir(source_path)
    for item in source_files:
        if item.endswith(tuple(extensions)):
            os.rename(source_path + item, destination_path + item)