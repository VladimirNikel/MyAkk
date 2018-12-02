#include "mainwindow.h"
#include "login_window.h"
#include <QApplication>
#include <QObject>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    Login_window lo;
    lo.show();
    QObject::connect(&lo,SIGNAL(openWindow()),&w,SLOT(showwin()));


    return a.exec();
}
