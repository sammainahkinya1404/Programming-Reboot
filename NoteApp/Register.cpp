#include "Register.h"
#include <QSqlQuery>
#include <QSqlError>
#include <QMessageBox>

Register::Register(QWidget *parent) : QWidget(parent) {
    QVBoxLayout *layout = new QVBoxLayout(this);

    usernameEdit = new QLineEdit(this);
    usernameEdit->setPlaceholderText("Username");
    layout->addWidget(usernameEdit);

    passwordEdit = new QLineEdit(this);
    passwordEdit->setPlaceholderText("Password");
    passwordEdit->setEchoMode(QLineEdit::Password);
    layout->addWidget(passwordEdit);

    QPushButton *registerButton = new QPushButton("Register", this);
    layout->addWidget(registerButton);

    connect(registerButton, &QPushButton::clicked, this, &Register::registerUser);

    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("database.db");

    if (!db.open()) {
        QMessageBox::critical(this, "Database Error", db.lastError().text());
    }

    QSqlQuery query;
    query.exec("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)");
}

Register::~Register() {
    db.close();
}

void Register::registerUser() {
    QString username = usernameEdit->text();
    QString password = passwordEdit->text();

    if (username.isEmpty() || password.isEmpty()) {
        QMessageBox::warning(this, "Input Error", "Please enter a username and password.");
        return;
    }

    QSqlQuery query;
    query.prepare("INSERT INTO users (username, password) VALUES (?, ?)");
    query.addBindValue(username);
    query.addBindValue(password);

    if (query.exec()) {
        QMessageBox::information(this, "Success", "User registered successfully.");
    } else {
        QMessageBox::critical(this, "Database Error", query.lastError().text());
    }
}

