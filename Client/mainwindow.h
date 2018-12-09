#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QNetworkAccessManager>

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
    QNetworkAccessManager *manager;
    //bool allowedWork=false;

public slots:
    void showwin();


private slots:
    void show_window_login();
    void replyFinished(QNetworkReply*);




    void on_addData_clicked();

    void on_update_clicked();

    void on_go_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
