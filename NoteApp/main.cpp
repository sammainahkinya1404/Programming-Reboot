#include <QApplication>
#include "MainWindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    MainWindow mainWindow;
    mainWindow.setWindowTitle("Welcome");
    mainWindow.resize(400, 300);
    mainWindow.show();

    return app.exec();
}

