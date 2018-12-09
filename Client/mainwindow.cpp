#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMenuBar>
#include <QAction>
#include "login_window.h"
#include "adddata.h"
#include <QDebug>
#include <QDesktopServices>
#include <QClipboard>
#include <QUrl>
#include <QNetworkAccessManager>
#include <QNetworkReply>


MainWindow::MainWindow(QWidget *parent, QString *name) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->name = name;

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

    manager = new QNetworkAccessManager(this);
    qDebug() << connect(manager, SIGNAL(finished(QNetworkReply*)), this, SLOT(replyFinished(QNetworkReply*)));


}
void MainWindow::showwin(){
    this->show();
    qDebug()<<"(mainwindows) name = "<<(*name);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::show_window_login(){

    Login_window login_wind(nullptr, name);
    login_wind.setModal(true);
    login_wind.exec();

}

//      http://192.168.1.7:8000/psswdmng/getauthseq/?username=vvovv


void MainWindow::on_addData_clicked(){
    addData a;
    a.setModal(true);
    a.exec();
}

void MainWindow::on_update_clicked()
{
    //отображение url
    QDesktopServices::openUrl(QUrl("http://185.228.234.173:3000"));
    QClipboard *clipboard = QApplication::clipboard();
    clipboard->setText("nen z ,sk");


}

void MainWindow::on_go_clicked()
{

    for(int i=0;i<1000;i++){
        QString request = ui->inputURL->text();
        manager->get(QNetworkRequest(QUrl(request)));
    }

    qDebug()<<"here";
}

void MainWindow::replyFinished(QNetworkReply* reply)
{
    qDebug()<<"error: "<<reply->error();
    QByteArray content = reply->readAll();

    qDebug()<<content;
    ui->textBrowser->setText(content);
}
