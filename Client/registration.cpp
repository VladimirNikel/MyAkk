#include "registration.h"
#include "ui_registration.h"


registration::registration(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::registration)
{
    ui->setupUi(this);
    ui->text->setText("");
    //connect(ui->pass1, SIGNAL(textChanged(QString)),this,SLOT(check()));
    //connect(ui->pass2, SIGNAL(textChanged(QString)),this,SLOT(check()));

}

registration::~registration()
{
    delete ui;
}

void registration::check(){
    if(ui->pass1->text()==ui->pass2->text()){
        QPixmap chec(":/photo/check.ico");
        ui->foto->setPixmap(chec);
        ui->foto->setScaledContents(true);
        ui->text->setText("");
    }
    else {
        QPixmap cros(":/photo/cross.ico");
        ui->foto->setPixmap(cros);
        ui->foto->setScaledContents(true);
        ui->text->setText(" ! Пароли не совпадают.");
    }
}

void registration::on_go_clicked()
{
    //тут запрос для создания нового пользователя
}
