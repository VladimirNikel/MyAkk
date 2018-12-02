#include "mainwindow.h"
#include "login_window.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    Login_window lo;
    lo.show();



    return a.exec();
}
