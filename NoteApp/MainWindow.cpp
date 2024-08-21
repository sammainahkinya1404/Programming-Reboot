#include "MainWindow.h"
#include "Register.h"
#include "Login.h"

MainWindow::MainWindow(QWidget *parent) : QWidget(parent) {
    QVBoxLayout *layout = new QVBoxLayout(this);

    QPushButton *registerButton = new QPushButton("Register", this);
    layout->addWidget(registerButton);

    QPushButton *loginButton = new QPushButton("Login", this);
    layout->addWidget(loginButton);

    connect(registerButton, &QPushButton::clicked, this, &MainWindow::openRegister);
    connect(loginButton, &QPushButton::clicked, this, &MainWindow::openLogin);
}

void MainWindow::openRegister() {
    Register *registerWindow = new Register();
    registerWindow->show();
}

void MainWindow::openLogin() {
    Login *loginWindow = new Login();
    loginWindow->show();
}

