#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0, QString *name = nullptr);
    ~MainWindow();
    QString *name;
    //bool allowedWork=false;

public slots:
    void showwin();


private slots:
    void show_window_login();




    void on_addData_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
