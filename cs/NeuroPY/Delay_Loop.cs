using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading;

namespace NeuroPY
{
    class Delay_Loop
    {
        string path = @"temp.txt";

        public void delayValue(string value)
        {
            bool load = true;


            while (load)
            {
                Thread.Sleep(1000);
                try
                {
                    if (File.ReadAllText(path) == value)
                    {
                        load = false;
                        File.WriteAllText(path, "");
                    }
                }
                catch { }
                
            }
        }

        public void delayNotValue()
        {
            bool load = true;


            while (load)
            {
                Thread.Sleep(1000);
                try
                {
                    if (File.ReadAllText(path) != "")
                    {
                        load = false;
                        File.WriteAllText(path, "");
                    }
                }
                catch { }

            }
        }

        public void delayRecord(string value)
        {
            bool load = true;


            while (load)
            {
                Thread.Sleep(1000);
                try
                {
                    if (File.ReadAllText(path) != ".")
                    {
                        load = false;
                        File.WriteAllText(path, value);
                    }
                }
                catch { }

            }
        }

        public string get_file_value_with_value(string value)
        {
            while (true)
            {
                Thread.Sleep(1000);
                try
                {
                    if (File.ReadAllText(path) != value)
                    {
                        return File.ReadAllText(path);
                    }
                }
                catch { }

            }
        }
    }
}
