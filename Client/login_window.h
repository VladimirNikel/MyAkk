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
    explicit Login_window(QWidget *parent = nullptr);
    ~Login_window();
    bool resultAutorization;
public slots:
    void button_enable();
    bool transferResultAutorization();

private slots:
    void on_buttonEntry_clicked();


private:
    Ui::Login_window *ui;
};

#endif // LOGIN_WINDOW_H
