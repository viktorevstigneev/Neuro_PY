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
using System.Windows.Threading;

namespace NeuroPY
{
    /// <summary>
    /// Логика взаимодействия для recognationPage.xaml
    /// </summary>
    public partial class recognationPage : Page
    {
        Frame frame1;

        public recognationPage(Frame frame)
        {
            InitializeComponent();
            frame1 = frame;
        }

        int counterOneTime2;
        DispatcherTimer counterOne2;

        int image_name = 0;
        private void counterOne2_Tick(object sender, EventArgs e)
        {

            try
            {
                image_name += 1;
                string path = System.IO.Path.GetFullPath($"../demo/recognition_video/output/frames/{image_name}.jpg");
                BitmapImage btm = new BitmapImage(new Uri(path, UriKind.Absolute));
                frame_pict.Source = btm;

            }
            catch
            {
                image_name -= 1;
            }



        }


        private void btn_start_recognation_Click(object sender, RoutedEventArgs e)
        {
            // передаём python данные
            Delay_Loop record = new Delay_Loop();
            record.delayRecord("recognation");

            Delay_Loop get_val = new Delay_Loop();
            image_name = Convert.ToInt32(get_val.get_file_value_with_value("recognation"));

            counterOne2 = new DispatcherTimer();
            counterOne2.Tick += new EventHandler(counterOne2_Tick);
            counterOne2.Interval = new TimeSpan(0, 0, 0, 0, 400);
            counterOne2.Start();
        }
    }
}
