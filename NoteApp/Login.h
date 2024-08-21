#ifndef LOGIN_H
#define LOGIN_H

#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QSqlDatabase>

class Login : public QWidget {
    Q_OBJECT

public:
    Login(QWidget *parent = nullptr);
    ~Login();

private slots:
    void loginUser();

private:
    QLineEdit *usernameEdit;
    QLineEdit *passwordEdit;
    QSqlDatabase db;
};

#endif // LOGIN_H

