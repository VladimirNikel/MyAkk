#include "adddata.h"
#include "ui_adddata.h"
#include <QString>
#include <QtSql>

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


}
