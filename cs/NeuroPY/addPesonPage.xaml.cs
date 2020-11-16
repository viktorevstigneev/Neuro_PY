using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization;
using System.Text;
using System.Threading;
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
    /// Логика взаимодействия для addPesonPage.xaml
    /// </summary>
    public partial class addPesonPage : Page
    {
        Frame frame1;
        int counterOneTime;
        DispatcherTimer counterOne;

        int counterOneTime2;
        DispatcherTimer counterOne2;

        public addPesonPage(Frame frame)
        {
            InitializeComponent();
            frame1 = frame;
        }

        int image_name = 0;
        string person_name;

        private void counterOne2_Tick(object sender, EventArgs e)
        {

            try
            {
                image_name += 1;
                string path = System.IO.Path.GetFullPath($"../demo/people/{person_name}/{image_name}.jpg");
                BitmapImage btm = new BitmapImage(new Uri(path, UriKind.Absolute));
                face_pict.Source = btm;
                counterOneTime--;

            }
            catch
            {
                image_name -= 1;
            }



        }

        private void counterOne_Tick(object sender, EventArgs e)
        {
            // code goes here

            if (counterOneTime > 0)
            {
                counterOneTime--;
                CounterLabel.Content = counterOneTime;
            }
            else
            {
                counterOne.Stop();
                string person_state = textbox_surname.Text + " " + textbox_name.Text + " " + textbox_middlename.Text + " " + textbox_group.Text + " " + textbox_curator.Text;
                person_name = textbox_surname.Text + " " + textbox_name.Text + " " + textbox_middlename.Text + "," + textbox_group.Text + "," + textbox_curator.Text;

                // передаём python данные
                Delay_Loop record = new Delay_Loop();
                record.delayRecord(person_state);

                counterOne2 = new DispatcherTimer();
                counterOne2.Tick += new EventHandler(counterOne2_Tick);
                counterOne2.Interval = new TimeSpan(0, 0, 0, 0, 400);
                counterOneTime2 = 30;
                counterOne2.Start();



            }
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            counterOne = new DispatcherTimer();
            counterOne.Tick += new EventHandler(counterOne_Tick);
            counterOne.Interval = new TimeSpan(0, 0, 1);

            counterOneTime = 5;
            counterOne.Start();

        }

        private void back_Click(object sender, RoutedEventArgs e)
        {

            // передаём python данные
            Delay_Loop record = new Delay_Loop();
            record.delayRecord("");
            mainMenuPage p = new mainMenuPage(frame1);
            frame1.Navigate(p);
        }
    }
}
