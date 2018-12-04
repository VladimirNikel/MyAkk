#ifndef ADDDATA_H
#define ADDDATA_H

#include <QDialog>

namespace Ui {
class addData;
}

class addData : public QDialog
{
    Q_OBJECT

public:
    explicit addData(QWidget *parent = nullptr, QString *name = nullptr);
    ~addData();
    QString *name;

private slots:
    void on_toolButton_clicked();

private:
    Ui::addData *ui;
};

#endif // ADDDATA_H
