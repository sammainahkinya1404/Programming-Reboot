#ifndef REGISTER_H
#define REGISTER_H

#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QSqlDatabase>

class Register : public QWidget {
    Q_OBJECT

public:
    Register(QWidget *parent = nullptr);
    ~Register();

private slots:
    void registerUser();

private:
    QLineEdit *usernameEdit;
    QLineEdit *passwordEdit;
    QSqlDatabase db;
};

#endif // REGISTER_H

