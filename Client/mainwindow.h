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
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    bool allowedWork=false;

private slots:
    void show_window_login();



private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
