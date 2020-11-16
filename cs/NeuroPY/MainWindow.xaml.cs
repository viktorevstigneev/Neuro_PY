using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;

namespace NeuroPY
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

            string path = @"temp.txt";

            //// Очищаем временный файл 
            //File.WriteAllText(path, "");

            //// открываем консоль и запускаем python скрипт
            //ProcessStartInfo psi;
            //psi = new ProcessStartInfo("cmd", @"/k py -3.6 main.py");
            //Process.Start(psi);

            // ждём, пока скрипт python выполнит свои действия 
            Delay_Loop dl = new Delay_Loop();
            dl.delayValue("loaded");

            SignInPage page = new SignInPage(MainFrame);
            MainFrame.Navigate(page);

        }

    }
}
