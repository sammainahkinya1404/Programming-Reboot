QT += core gui sql
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = NoteApp
TEMPLATE = app

SOURCES += main.cpp \
    NoteApp.cpp \
    Register.cpp \
    Login.cpp \
    MainWindow.cpp

HEADERS += NoteApp.h \
    Register.h \
    Login.h \
    MainWindow.h

