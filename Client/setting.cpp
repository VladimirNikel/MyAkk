#include "setting.h"
#include "ui_setting.h"

Setting::Setting(QWidget *parent, QString *ipHost) :
    QDialog(parent),
    ui(new Ui::Setting)
{
    ui->setupUi(this);
    this->ipHost = ipHost;
    ui->ipHost->setText((*ipHost));


}

Setting::~Setting()
{
    delete ui;
}

void Setting::on_pushButton_clicked()
{
    *ipHost = ui->ipHost->text();
}
