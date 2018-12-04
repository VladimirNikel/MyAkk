#include "adddata.h"
#include "ui_adddata.h"
#include <QString>
#include <QtSql>
#include <QSqlQuery>


addData::addData(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::addData)
{
    ui->setupUi(this);






}

addData::~addData()
{
    delete ui;
}

void addData::on_toolButton_clicked()
{
    QString resource = ui->adResource->text();
    QString login = ui->addLogin->text();
    QString pass = ui->addPassword->text();


    //Подключаем базу данных
    QSqlDatabase db;
    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("Password_manager_db.sqlite3");
    db.open();

    //Осуществляем запрос
    QSqlQuery query;
    query.exec("SELECT * FROM psswdmng_user");


    /*
    //Выводим значения из запроса
    while (query.next())    {
        QString _id = query.value(0).toString();
        QString name = query.value(1).toString();
        QString mast_pass = query.value(2).toString();
        QString open_key = query.value(3).toString();

        ui->textEdit->insertPlainText(_id+" "+name+" "+mast_pass+" "+open_key+"\n");
    }
    */

}
