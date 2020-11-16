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
    /// Логика взаимодействия для mainMenuPage.xaml
    /// </summary>
    public partial class mainMenuPage : Page
    {
        Frame frame1;
        public mainMenuPage(Frame frame)
        {
            InitializeComponent();
            frame1 = frame;

        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            // передаём python данные
            Delay_Loop record = new Delay_Loop();
            record.delayRecord("adding_a_new_face");

            addPesonPage s = new addPesonPage(frame1);
            frame1.Navigate(s);
        }

        private void recognation_Click(object sender, RoutedEventArgs e)
        {
            recognationPage recognationpage = new recognationPage(frame1);
            frame1.Navigate(recognationpage);
        }

        private void search_Click(object sender, RoutedEventArgs e)
        {
            searchPersonPage searchPersonPage = new searchPersonPage(frame1);
            frame1.Navigate(searchPersonPage);
        }
    }
}
