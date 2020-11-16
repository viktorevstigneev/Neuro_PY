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
    /// Логика взаимодействия для SignInPage.xaml
    /// </summary>
    public partial class SignInPage : Page
    {
        Frame frame;

        public SignInPage( Frame frame)
        {
            InitializeComponent();
            this.frame = frame;
            
        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {
            SignUp su = new SignUp(frame);
            frame.Navigate(su);
        }
    }
}
