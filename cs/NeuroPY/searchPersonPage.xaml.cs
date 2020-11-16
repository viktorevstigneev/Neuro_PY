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
    /// Логика взаимодействия для searchPersonPage.xaml
    /// </summary>
    public partial class searchPersonPage : Page
    {
        Frame frame1;
        public searchPersonPage(Frame frame)
        {
            InitializeComponent();
            frame1 = frame;
        }

        private void r_MouseEnter(object sender, MouseEventArgs e)
        {
            r.Height = 150;
        }

        private void r_MouseLeave(object sender, MouseEventArgs e)
        {
            r.Height = 30;
        }
    }
}
