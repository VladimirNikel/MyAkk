#ifndef LOGIN_WINDOW_H
#define LOGIN_WINDOW_H

#include <QDialog>

namespace Ui {
class Login_window;
}

class Login_window : public QDialog
{
    Q_OBJECT

public:
    explicit Login_window(QWidget *parent = nullptr, QString *name = nullptr);
    ~Login_window();
    QString *name;


signals:
    void openWindow();


public slots:
    void button_enable();


private slots:
    void on_buttonEntry_clicked();


    void on_pushButton_clicked();

private:
    Ui::Login_window *ui;
};

#endif // LOGIN_WINDOW_H
