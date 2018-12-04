#include "mainwindow.h"
#include "login_window.h"
#include <QApplication>
#include <QObject>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QString *name = new QString;
    MainWindow w(nullptr, name);
    Login_window lo(nullptr, name);
    lo.show();
    QObject::connect(&lo,SIGNAL(openWindow()),&w,SLOT(showwin()));


    return a.exec();
}
