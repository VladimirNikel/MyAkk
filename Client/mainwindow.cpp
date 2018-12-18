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
#include "setting.h"
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QtSql>


MainWindow::MainWindow(QWidget *parent, QString *name, QString *ipHost) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->name = name;
    this->ipHost = ipHost;


    //================действия=для=меню=Файл=====================
    connect(ui->login, SIGNAL(triggered()), this, SLOT(show_window_login()));
    connect(ui->account_setting, SIGNAL(triggered()), this, SLOT(action()));
    connect(ui->check_update, SIGNAL(triggered()), this, SLOT(action()));
    connect(ui->setting, SIGNAL(triggered()), this, SLOT(show_setting_window()));
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





    ui->textBrowser_2->setText("Подсказка:\n\nЕсли в отображаемом списке не была найдена интересующая Вас запись - совершите её поиск по URL-адресу.");
    //количество столбцов
    ui->tableWidget->setColumnCount(2);
    ui->tableWidget->setHorizontalHeaderLabels(QStringList()<<"URL-адрес"<<"Логин");

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

void MainWindow::show_setting_window(){
    Setting win(nullptr, ipHost);
    win.setModal(true);
    win.exec();
}

//      http://192.168.1.7:8000/psswdmng/getauthseq/?username=vvovv


void MainWindow::on_addData_clicked(){
    addData a;
    a.setModal(true);
    a.exec();
}

void MainWindow::print_tip(){
    //Подсказка: Если в отображаемом списке не была найдена интересующая Вас запись - совершите её поиск по URL-адресу.
    ui->textBrowser_2->setText("Подсказка:\n\nЕсли в отображаемом списке не была найдена интересующая Вас запись - совершите её поиск по URL-адресу.");

}

void MainWindow::on_update_clicked()
{
    //обновление таблицы
    //количество строк
    ui->tableWidget->setRowCount(25);
    ui->tableWidget->setColumnWidth(0,289);
    ui->tableWidget->setColumnWidth(1,289);

    QSqlDatabase db;
    QSqlDatabase::removeDatabase("qt_sql_default_connection");
    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("D:/Documents/Qt/1 prototype/prototype/Password_manager_db.sqlite3");
    if(!db.open()){
        qDebug()<<db.lastError().text();
    }
    else {
        qDebug() << "Success!";
    }

    //Осуществляем запрос
    QSqlQuery query;
    query.prepare("SELECT r.URL, l.Login FROM psswdmng_login l, psswdmng_resource r  "
                  "WHERE (SELECT pair_id FROM (SELECT * FROM psswdmng_pair WHERE pair_id IN ("
                  "SELECT pair_id_id FROM psswdmng_main_record WHERE user_id_id = ("
                  "SELECT user_id FROM psswdmng_user WHERE User_name = :us_name))) p WHERE (p.resource_id_id = r.resource_id) AND (p.login_id_id = l.login_id))");
    query.bindValue(":us_name", *name);
    query.exec();

    int i=0;
    while(query.next()){
        QString URL = query.value(0).toString();
        QString login = query.value(1).toString();
        QTableWidgetItem *itmURL = new QTableWidgetItem(tr("%1").arg(URL));
        QTableWidgetItem *itmLogin = new QTableWidgetItem(login);
        ui->tableWidget->setItem(i,0,itmURL);
        ui->tableWidget->setItem(i,1,itmLogin);
        i++;
    }
    db.close();


    /*
    //QString URLfull =
    QDesktopServices::openUrl(QUrl("http://185.228.234.173:3000"));
    QClipboard *clipboard = QApplication::clipboard();
    clipboard->setText("nen z ,sk");

    */
}

void MainWindow::on_go_clicked()
{

    for(int i=0;i<1;i++){
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
    //ui->textBrowser->setText(content);
}
