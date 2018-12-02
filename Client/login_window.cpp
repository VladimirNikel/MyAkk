#include "login_window.h"
#include "ui_login_window.h"
#include <QtSql>
#include <QMessageBox>

Login_window::Login_window(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Login_window)
{
    ui->setupUi(this);
    ui->inputLogin->setText("");
    ui->inputPassword->setText("");
    ui->buttonEntry->setEnabled(false);
    connect(ui->inputLogin,SIGNAL(textChanged(QString)),this,SLOT(button_enable()));
    connect(ui->inputPassword,SIGNAL(textChanged(QString)),this,SLOT(button_enable()));

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

bool Login_window::transferResultAutorization(){
    return resultAutorization;
}

void Login_window::on_buttonEntry_clicked()
{
    QString login = ui->inputLogin->text();
    QString password = ui->inputPassword->text();

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
        close();
    }
}
