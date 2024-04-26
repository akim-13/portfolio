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
using System.Windows.Markup;
using System.Windows.Input;

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
                ActiveLines.Add(WorkLine);
            }
            if (outputList == "Nothing")
            {
                LineGraph.Visibility = System.Windows.Visibility.Hidden;
            }
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
                Labels = new[] { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" },
                MinValue = 0
            });

            Axis axisY = (Axis)LineGraph.AxisY[0];
            axisY.MaxValue = 10;
            axisY.Separator.Step = 1;
            LineGraph.Update(true);

            GenerateValues(DateTime.Now.AddDays(-1).Date, DateTime.Now.Date, ActiveLines);
        }

        private void GenerateValues(DateTime StartTimeFrame, DateTime EndTimeFrame, List<LineSeries> ActiveLines)
        {
            SeriesCollection series = new SeriesCollection();
            LineSeries sleepline = new LineSeries();
            LineSeries workline = new LineSeries();
            LineSeries waterline = new LineSeries();
            LineSeries stepsline = new LineSeries();

            // Sort the list by Date
            this.LineGraph.Series.Clear();
            if (ActiveLines.Contains(SleepLine))
            {
                sleepline.LineSmoothness = 0;
                sleepline.Title = "Sleep";
                sleepline.LabelPoint = point => $"{point.Y:N1}";
                var Data = Database.Instance.GetUserActivities(StartTimeFrame, EndTimeFrame, "UserSleep");
                var dataList = Data.ToList();
                dataList = dataList.OrderBy(d => d.Date).ToList();
                List<float> values = new List<float>();
                for (int loop = 0; loop < dataList.Count; loop++)
                {
                    values.Add(dataList[loop].Value);
                }
                IChartValues list = new ChartValues<float>(values);
                sleepline.Values = list;
                series.Add(sleepline);
            }
            if (ActiveLines.Contains(StepsLine))
            {
                stepsline.LineSmoothness = 0;
                stepsline.Title = "Steps (1000)";
                var Data = Database.Instance.GetUserActivities(StartTimeFrame, EndTimeFrame, "UserSteps");
                var dataList = Data.ToList();
                dataList = dataList.OrderBy(d => d.Date).ToList();
                List<float> values = new List<float>();
                for (int loop = 0; loop < dataList.Count; loop++)
                {
                    values.Add(dataList[loop].Value / 1000);
                }
                IChartValues list = new ChartValues<float>(values);
                stepsline.Values = list;
                series.Add(stepsline);
            }
            if (ActiveLines.Contains(WaterLine))
            {
                waterline.LineSmoothness = 0;
                waterline.Title = "Water";
                waterline.LabelPoint = point => $"{point.Y:N1}";// Multiply Y value by 1000 and format to 2 decimal places
                var Data = Database.Instance.GetUserActivities(StartTimeFrame, EndTimeFrame, "UserWater");
                var dataList = Data.ToList();
                dataList = dataList.OrderBy(d => d.Date).ToList();
                List<float> values = new List<float>();
                for (int loop = 0; loop < dataList.Count; loop++)
                {
                    values.Add(dataList[loop].Value);
                }
                IChartValues list = new ChartValues<float>(values);
                waterline.Values = (list);
                series.Add(waterline);
            }
            if (ActiveLines.Contains(WorkLine))
            {
                workline.LineSmoothness = 0;
                workline.Title = "Work";
                workline.LabelPoint = point => $"{point.Y:N1}";// Multiply Y value by 1000 and format to 2 decimal places
                var Data = Database.Instance.GetUserActivities(StartTimeFrame, EndTimeFrame, "UserWork");
                var dataList = Data.ToList();
                dataList = dataList.OrderBy(d => d.Date).ToList();
                List<float> values = new List<float>();
                for (int loop = 0; loop < dataList.Count; loop++)
                {
                    values.Add(dataList[loop].Value);
                }
                IChartValues list = new ChartValues<float>(values);
                workline.Values = (list);
                series.Add(workline);
            }
            LineGraph.Series = series;



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
                GenerateValues(DateTime.Now.AddDays(-1).Date, DateTime.Now.Date, ActiveLines);
            }
            else if (cbi.Content.ToString() == "week")
            {
                string[] daysArray = new string[7];

                for (int loop = 6; loop >= 0; loop--)
                {
                    daysArray[6 - loop] = DateTime.Now.AddDays(-loop).DayOfWeek.ToString();
                }

                xTitle = "Week";
                xLabels = daysArray;
                xMaxval = 6;
                GenerateValues(DateTime.Now.AddDays(-6).Date, DateTime.Now.Date, ActiveLines);
            }
            else if (cbi.Content.ToString() == "month")
            {
                xTitle = "Month";
                DateTime startDate = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1);
                DateTime endDate = startDate.AddMonths(1).AddDays(-1);
                xMaxval = endDate.Day - 1;
                xLabels = new string[endDate.Day];
                for (int loop = 0; loop < endDate.Day; loop++)
                {
                    xLabels[loop] = (loop + 1).ToString();
                }
                GenerateValues(startDate, endDate, ActiveLines);

            }
            else if (cbi.Content.ToString() == "year")
            {
                xTitle = "Year";
                xLabels = new string[] { "Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec" };
                xMaxval = 11;
                int[] MonthAvg = new int[12];

                this.LineGraph.Series.Clear();
                SeriesCollection series = new SeriesCollection();
                LineSeries sleepline = new LineSeries();
                LineSeries workline = new LineSeries();
                LineSeries waterline = new LineSeries();
                LineSeries stepsline = new LineSeries();

                if (ActiveLines.Contains(SleepLine))
                {
                    sleepline.LineSmoothness = 0;
                    sleepline.Title = "Sleep";
                    sleepline.Values = new ChartValues<double> { };
                    sleepline.LabelPoint = point => $"{point.Y:N1}";// Multiply Y value by 1000 and format to 2 decimal places
                    series.Add(sleepline);
                }
                if (ActiveLines.Contains(StepsLine))
                {
                    stepsline.LineSmoothness = 0;
                    stepsline.Title = "Steps (1000)";
                    stepsline.Values = new ChartValues<double> { };
                    series.Add(stepsline);
                }
                if (ActiveLines.Contains(WaterLine))
                {
                    waterline.LineSmoothness = 0;
                    waterline.Title = "Water";
                    waterline.LabelPoint = point => $"{point.Y:N1}";// Multiply Y value by 1000 and format to 2 decimal places
                    waterline.Values = new ChartValues<double> { };
                    series.Add(waterline);
                }
                if (ActiveLines.Contains(WorkLine))
                {
                    workline.LineSmoothness = 0;
                    workline.Title = "Work";
                    workline.LabelPoint = point => $"{point.Y:N1}";// Multiply Y value by 1000 and format to 2 decimal places
                    workline.Values = new ChartValues<double> { };
                    series.Add(waterline);
                }

                for (int loop = 0; loop <= 11; loop++)
                {
                    DateTime startDate = new DateTime(DateTime.Now.Year, loop + 1, 1);
                    // Finding the end date of the month
                    DateTime endDate = startDate.AddMonths(1).AddDays(-1);

                    // Sort the list by Date
                    if (ActiveLines.Contains(SleepLine))
                    {
                        var Data = Database.Instance.GetUserActivities(startDate, endDate, "UserSleep");
                        var dataList = Data.ToList();
                        dataList = dataList.OrderBy(d => d.Date).ToList();
                        double avg = 0;
                        for (int loop2 = 0; loop2 < dataList.Count; loop2++)
                        {
                            avg += dataList[loop2].Value;
                        }
                        avg = avg / dataList.Count;
                        sleepline.Values.Add(avg);
                    }
                    if (ActiveLines.Contains(StepsLine))
                    {
                        var Data = Database.Instance.GetUserActivities(startDate, endDate, "UserSteps");
                        var dataList = Data.ToList();
                        dataList = dataList.OrderBy(d => d.Date).ToList();
                        double avg = 0;
                        for (int loop2 = 0; loop2 < dataList.Count; loop2++)
                        {
                            avg += (dataList[loop2].Value / 1000);
                        }
                        avg = avg / dataList.Count;
                        stepsline.Values.Add(avg);
                    }
                    if (ActiveLines.Contains(WaterLine))
                    {
                        var Data = Database.Instance.GetUserActivities(startDate, endDate, "UserWater");
                        var dataList = Data.ToList();
                        dataList = dataList.OrderBy(d => d.Date).ToList();
                        double avg = 0;
                        for (int loop2 = 0; loop2 < dataList.Count; loop2++)
                        {
                            avg += (dataList[loop2].Value);
                        }
                        avg = avg / dataList.Count;
                        waterline.Values.Add(avg);
                    }
                    if (ActiveLines.Contains(WorkLine))
                    {
                        var Data = Database.Instance.GetUserActivities(startDate, endDate, "UserWork");
                        var dataList = Data.ToList();
                        dataList = dataList.OrderBy(d => d.Date).ToList();
                        double avg = 0;
                        for (int loop2 = 0; loop2 < dataList.Count; loop2++)
                        {
                            avg += (dataList[loop2].Value);
                        }
                        avg = avg / dataList.Count;
                        waterline.Values.Add(avg);
                    }
                    LineGraph.Series = series;



                }
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
