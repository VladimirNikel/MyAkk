#include "login_window.h"
#include "ui_login_window.h"
#include <QtSql>
#include <QMessageBox>
#include <QCryptographicHash>
#include <QtSql>
#include <QSqlQuery>


Login_window::Login_window(QWidget *parent, QString *name):
    QDialog(parent),
    ui(new Ui::Login_window)
{
    ui->setupUi(this);
    ui->inputLogin->setText("");
    ui->inputPassword->setText("");
    ui->buttonEntry->setEnabled(false);
    connect(ui->inputLogin,SIGNAL(textChanged(QString)),this,SLOT(button_enable()));
    connect(ui->inputPassword,SIGNAL(textChanged(QString)),this,SLOT(button_enable()));
    this->name = name;

}


void Login_window::button_enable(){
    if(ui->inputPassword->text() != "" && ui->inputLogin->text() != ""){
        ui->buttonEntry->setEnabled(true);
    }
    else ui->buttonEntry->setEnabled(false);
}


Login_window::~Login_window()
{
    delete ui;
}

void Login_window::on_buttonEntry_clicked()
{
    QString login = ui->inputLogin->text();
    QString password = ui->inputPassword->text();

    //получение хэша пароля
    QByteArray ba = password.toUtf8();
    //переменная для хранения хэша в
    QByteArray pass_hash = QCryptographicHash::hash(ba,QCryptographicHash::Sha512);
    qDebug()<<pass_hash;

    //Подключаем базу данных
    QSqlDatabase db;
    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("D:/Documents/Qt/1 prototype/prototype/Password_manager_db.sqlite3");
    if(!db.open()){
        qDebug()<<db.lastError().text();
    }
    else {
        qDebug() << "Success!";
    }


    QSqlQuery query;
    query.prepare("SELECT Master_password_hash "
                  "FROM psswdmng_user "
                  "WHERE User_name = :us_name");
    //query.addBindValue(login);
    query.bindValue(":us_name", login);
    query.exec();
    qDebug()<<query.result();

    query.first();
    qDebug()<<"Ответ на запрос "<<(query.value(0)).toByteArray();

    QByteArray hash_base = (query.value(0)).toByteArray();
    qDebug()<<hash_base;

    if(hash_base == pass_hash){
        QMessageBox::information(this, "Вход осуществлен", "Вы успешно авторизированны.");
        *name = login;
        emit openWindow();
        db.close();
        close();
    }
    else {
        QMessageBox::warning(this,"Вход не выполнен","Проверьте введенные данные и повторите попытку.");
        *name = "";
    }





/*
    //:/db/Password_manager_db.sqlite3
    //Осуществляем запрос
    QSqlQuery query;
    query.prepare("INSERT INTO psswdmng_user (User_name, Master_password_hash, Open_key) "
                  "VALUES (:login, :pass_hash, :ba)");
    query.bindValue(":login", login);
    query.bindValue(":pass_hash", pass_hash);
    query.bindValue(":ba", ba);
    query.exec();

    qDebug()<<db.lastError().text();
*/



/*
    if ((login == "Nikel") && (password == "12345")){
        QMessageBox::information(this, "Вход осуществлен", "Вы успешно авторизированны.");
        resultAutorization = true;
        emit openWindow();
    }
    else {
        QMessageBox::warning(this,"Вход не выполнен","Проверьте введенные данные и повторите попытку.");
        resultAutorization = false;
    }
    if (resultAutorization == true) {
        db.close();
        close();
    }

*/
}
