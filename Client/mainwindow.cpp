#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMenuBar>
#include <QAction>
#include "login_window.h"
#include "adddata.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    //================действия=для=меню=Файл=====================
    connect(ui->login, SIGNAL(triggered()), this, SLOT(show_window_login()));
    connect(ui->account_setting, SIGNAL(triggered()), this, SLOT(action()));
    connect(ui->check_update, SIGNAL(triggered()), this, SLOT(action()));
    //===========================================================

    //================действия=для=меню=Правка====================
    connect(ui->unhide, SIGNAL(triggered()), this, SLOT(action()));
    connect(ui->hide, SIGNAL(triggered()), this, SLOT(action()));
    connect(ui->change_data, SIGNAL(triggered()), this, SLOT(action()));
    connect(ui->add_data, SIGNAL(triggered()), this, SLOT(on_addData_clicked()));
    //===========================================================

    //==========действия=для=меню=Резервное копирование==========
    connect(ui->perform_backup, SIGNAL(triggered()), this, SLOT(action()));
    //===========================================================

    //==================действия=для=меню=Вид====================
    connect(ui->perform_backup, SIGNAL(triggered()), this, SLOT(action()));
    //===========================================================
    //================действия=для=меню=Помощь===================
    connect(ui->perform_backup, SIGNAL(triggered()), this, SLOT(action()));
    //===========================================================





}
void MainWindow::showwin(){
    this->show();
}


MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::show_window_login(){
    Login_window login_wind;
    login_wind.setModal(true);
    login_wind.exec();

}




void MainWindow::on_addData_clicked(){
    addData a;
    a.setModal(true);
    a.exec();
}
