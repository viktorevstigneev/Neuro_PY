using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace NeuroPY
{
    /// <summary>
    /// Логика взаимодействия для SignUp.xaml
    /// </summary>
    public partial class SignUp : Page
    {
        Frame frame1;

        public SignUp(Frame frame)
        {
            InitializeComponent();
            frame1 = frame;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
           SignInPage s = new SignInPage(frame1);
            frame1.Navigate(s);
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            mainMenuPage p = new mainMenuPage(frame1);
            frame1.Navigate(p);
        }
    }
}
