from PyQt5.QtWidgets import \
    QApplication, \
    QWidget, \
    QPushButton, \
    QLabel, \
    QListWidget, \
    QTextEdit,\
    QInputDialog, \
    QHBoxLayout, \
    QVBoxLayout,\
    QMessageBox

import json

app = QApplication([])

'''Интерфейс приложения'''
# параметры окна приложения
notes_win = QWidget()
notes_win.setWindowTitle('Notes')
notes_win.resize(600, 400)

# виджеты окна приложения
list_notes = QListWidget()
list_notes_label = QLabel('Notes list')

button_create = QPushButton('Create note')  # появляется окно с полем "Введите имя заметки"
button_delete = QPushButton('Delete Note')
button_save = QPushButton('Save note')

field_text = QTextEdit()

# расположение виджетов по лэйаутам
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_create)
row_1.addWidget(button_delete)

row_2 = QHBoxLayout()
row_2.addWidget(button_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

'''Работа с текстом заметки'''
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name: ")
    if ok and note_name != "":
        notes[note_name] = {"text": ""}
        list_notes.addItem(note_name)

def show_note():
    # получаем текст из заметки с выделенным названием и отображаем его в поле редактирования
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["text"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["text"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        message_box = QMessageBox()
        message_box.setWindowTitle("Warning")
        message_box.setText("No note for saving!")
        message_box.exec_()

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        message_box = QMessageBox()
        message_box.setWindowTitle("Warning")
        message_box.setText("No note for deleting!")
        message_box.exec_()


'''Запуск приложения'''
# подключение обработки событий
list_notes.itemClicked.connect(show_note)
button_create.clicked.connect(add_note)
button_delete.clicked.connect(del_note)
button_save.clicked.connect(save_note)

# запуск приложения
notes_win.show()

with open("notes_data.json", "r", encoding="UTF-8") as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()
