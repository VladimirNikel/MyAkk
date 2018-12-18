#ifndef SETTING_H
#define SETTING_H

#include <QDialog>

namespace Ui {
class Setting;
}

class Setting : public QDialog
{
    Q_OBJECT

public:
    explicit Setting(QWidget *parent = nullptr, QString *ipHost = nullptr);
    ~Setting();
    QString *ipHost;

private slots:
    void on_pushButton_clicked();

private:
    Ui::Setting *ui;
};

#endif // SETTING_H