using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Windows.Controls;
using LiveCharts.Wpf;
using System.Windows.Media;
using LiveCharts;
using Windows.Foundation.Collections;
using LiveCharts.Wpf.Charts.Base;
using System.ComponentModel;
using System.Xml.Linq;
using PI_Systems.GUIs.HelperUserControls;

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for Graphs.xaml
    /// </summary>
    public partial class Graphs : UserControl
    {
        ActivityType[] activities;
        List<LineSeries> ActiveLines = new List<LineSeries>(); // tuple???????
        public Graphs(params CheckBox[] checkBoxes)
        {
            InitializeComponent();

            //Ollie: Setting up stuff for the graph such as xAxis and COlour of legend
            LineGraph.ChartLegend.Foreground = new SolidColorBrush(Colors.White);
            LineGraph.AxisX.Clear();
            DataContext = this;
            // Customize X-axis labels
            LineGraph.AxisX.Add(new Axis
            {
                Title = "Day",
                Labels = new[] { "Yesterday", "Today" }
            });
            Axis axisX = (Axis)LineGraph.AxisX[0];
            axisX.MaxValue = 1;
            axisX.Separator.Step = 1;
            LineGraph.AxisY.Clear();
            DataContext = this;
            LineGraph.AxisY.Add(new Axis
            {
                Labels = new[] {"0","1","2","3","4","5","6","7","8","9","10"}
            });

            Axis axisY = (Axis)LineGraph.AxisY[0];
            axisY.MaxValue = 10;
            axisY.Separator.Step = 1;
            LineGraph.Update(true);
            GenerateValues(-1, ActiveLines);

            activities = checkBoxes.Where(c => c.IsChecked == true).Select(c => (ActivityType)c.Tag).ToArray();
            string outputList = activities.Length == 0 ? "Nothing" : string.Join(", ", activities);
            label.Content = $"You want to see these graph(s): {outputList}";

            //Ollie: Making sure the LG only shows the appropriate lines. I know it's poorly coded but I couldn't think of a simpler way rn
            if (outputList.Contains("Steps"))
            {
                StepsLine.Visibility = System.Windows.Visibility.Visible;
                ActiveLines.Add(StepsLine);
            }
            if (outputList.Contains("Water"))
            {
                WaterLine.Visibility = System.Windows.Visibility.Visible;
                ActiveLines.Add(WaterLine);
            }
            if (outputList.Contains("Sleep"))
            {
                SleepLine.Visibility = System.Windows.Visibility.Visible;
                ActiveLines.Add(SleepLine);
            }
            if (outputList.Contains("Work"))
            {
                WorkLine.Visibility = System.Windows.Visibility.Visible;
                //ActiveLines.Add((WorkLine, typeof(UserWork)));
            }
            if (outputList == "Nothing")
            {
                LineGraph.Visibility = System.Windows.Visibility.Hidden;
            }
        }

        private void GenerateValues(int TimeFrame, List<LineSeries> ActiveLines)
        {
            this.LineGraph.Series.Clear();
            SeriesCollection series = new SeriesCollection();
            LineSeries sleepline = new LineSeries();
            LineSeries workline = new LineSeries();
            LineSeries waterline = new LineSeries();
            LineSeries stepsline = new LineSeries();

            if (ActiveLines.Contains(SleepLine))
            {
                var Data = Database.Instance.GetUserActivities<UserSleep>(DateTime.Now.AddDays(TimeFrame).Date, DateTime.Now.Date);
                List<float> values = new List<float>();
                for (int loop = 0; loop < Data.Length; loop++)
                {
                    values.Add(Data[loop].SleepHours);
                }
                IChartValues list = new ChartValues<float>(values);
                sleepline.Values = list;
                series.Add(sleepline);
            }
            if (ActiveLines.Contains(StepsLine))
            {
                var Data = Database.Instance.GetUserActivities<UserSteps>(DateTime.Now.AddDays(TimeFrame).Date, DateTime.Now.Date);
                List<float> values = new List<float>();
                for (int loop = 0; loop < Data.Length; loop++)
                {
                    values.Add(Data[loop].Steps / 1000);
                }
                IChartValues list = new ChartValues<float>(values);
                stepsline.Values = list;
                series.Add(stepsline);
            }
            if (ActiveLines.Contains(WaterLine))
            {
                var Data = Database.Instance.GetUserActivities<UserWater>(DateTime.Now.AddDays(TimeFrame).Date, DateTime.Now.Date);
                List<float> values = new List<float>();
                for (int loop = 0; loop < Data.Length; loop++)
                {
                    values.Add(Data[loop].LitresDrank);
                }
                IChartValues list = new ChartValues<float>(values);
                waterline.Values = (list);
                series.Add(waterline);
            }
            LineGraph.Series = series;
            /*
            if (ActiveLines.Contains(WorkLine))
            {
                WorkLine.Values.Clear();
                var Data = Database.Instance.GetUserActivities<UserWork>(DateTime.Now.AddDays(TimeFrame).Date, DateTime.Now.Date);
                float[] values = new float[Data.Length];
                for (int loop2 = 0; loop2 < Data.Length; loop2++)
                {
                    values[loop2] = Data[loop2].WorkDone??;
                }
                IChartValues list = new ChartValues<float>(values);
                WorkLine.Values = list;
            }*/

        }
        
        private void GoalTimeframe_Changed(object sender, SelectionChangedEventArgs e)
        {
            ComboBox cb = (ComboBox)sender;
            // James: The SelctionChanged calls this function whenever the selection changes (duh) but this also countswhenloading
            // the page, so we gotta include the if statement to ignore this case.
            if (!cb.IsLoaded)
            {
                return;
            }
            ComboBoxItem cbi = (ComboBoxItem)cb.SelectedItem;

            //Ollie: Updating the graph accordingly so it shows the correct time scale on the Xaxis
            // I also have to change the actual scale of the xaxis (this was such a pain to learn to do)


            string xTitle = "";
            string[] xLabels = new string[] { };
            int xMaxval = 0;
            if (cbi.Content.ToString() == "day")
            {
                xTitle = "Day";
                xLabels = new string[] { "Yesterday", "Today" };
                xMaxval = 1;
                GenerateValues(-1, ActiveLines);
            }
            else if (cbi.Content.ToString() == "week")
            {
                DayOfWeek currentDayOfWeek = DateTime.Now.DayOfWeek;
                string[] daysArray = new string[7];

                for (int i = daysArray.Length - 1; i >= 0; i--)
                {
                    daysArray[i] = currentDayOfWeek.ToString();
                    currentDayOfWeek = (DayOfWeek)(((int)currentDayOfWeek + 1) % 7);
                }

                xTitle = "Week";
                xLabels = daysArray;
                xMaxval = 6;
                GenerateValues(-7, ActiveLines);
            }
            else if (cbi.Content.ToString() == "month")
            {
                xTitle = "Last 30 Days";
                xMaxval = 29;

                xLabels = new string[30];
                for (int loop = 0; loop < 30; loop++)
                {
                    xLabels[loop] = (loop + 1).ToString();
                }
                GenerateValues(-30, ActiveLines);

            }
            else if (cbi.Content.ToString() == "year")
            {
                xTitle = "Year";
                xLabels = new string[] { "Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec" };
                xMaxval = 11;
                //god help me
            }
            LineGraph.AxisX.Clear();
            DataContext = this;
            LineGraph.AxisX.Add(new Axis
            {
                Title = xTitle,
                Labels = xLabels
            });

            Axis axisX = (Axis)LineGraph.AxisX[0];
            axisX.MaxValue = xMaxval;
            axisX.Separator.Step = 1;
            LineGraph.Update(true);
            Trace.WriteLine(cbi.Content.ToString());
        }
    }

}
