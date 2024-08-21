#ifndef NOTEAPP_H
#define NOTEAPP_H

#include <QWidget>
#include <QTextEdit>
#include <QPushButton>
#include <QVBoxLayout>

class NoteApp : public QWidget {
    Q_OBJECT

public:
    NoteApp(QWidget *parent = nullptr);

private slots:
    void saveNote();

private:
    QTextEdit *noteEditor;
};

#endif // NOTEAPP_H

