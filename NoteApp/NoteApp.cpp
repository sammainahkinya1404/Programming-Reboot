#include "NoteApp.h"
#include <QFileDialog>
#include <QFile>
#include <QTextStream>
#include <QMessageBox>

NoteApp::NoteApp(QWidget *parent) : QWidget(parent) {
    QVBoxLayout *layout = new QVBoxLayout(this);

    noteEditor = new QTextEdit(this);
    layout->addWidget(noteEditor);

    QPushButton *saveButton = new QPushButton("Save Note", this);
    layout->addWidget(saveButton);

    connect(saveButton, &QPushButton::clicked, this, &NoteApp::saveNote);
}

void NoteApp::saveNote() {
    QString fileName = QFileDialog::getSaveFileName(this, "Save Note", "", "Text Files (*.txt);;All Files (*)");
    if (!fileName.isEmpty()) {
        QFile file(fileName);
        if (file.open(QFile::WriteOnly | QFile::Text)) {
            QTextStream out(&file);
            out << noteEditor->toPlainText();
            file.close();
            QMessageBox::information(this, "Success", "Note saved successfully.");
        } else {
            QMessageBox::warning(this, "Error", "Could not save the note.");
        }
    }
}

