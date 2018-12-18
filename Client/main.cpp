#include "mainwindow.h"
#include "login_window.h"
#include <QApplication>
#include <QObject>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    //переменные
    QString *name = new QString;
    QString *ipHost = new QString;
    *ipHost = "http://192.168.1.13:8000";

    MainWindow w(nullptr, name, ipHost);
    Login_window lo(nullptr, name, ipHost);
    lo.show();
    QObject::connect(&lo,SIGNAL(openWindow()),&w,SLOT(showwin()));


    return a.exec();
}
