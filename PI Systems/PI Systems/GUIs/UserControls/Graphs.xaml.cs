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

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for Graphs.xaml
    /// </summary>
    public partial class Graphs : UserControl
    {
        ActivityType[] activities;

        public Graphs(params CheckBox[] checkBoxes)
        {
            InitializeComponent();

            //Ollie: Setting up stuff for the graph such as xAxis and COlour of legend
            LineGraph.ChartLegend.Foreground = new SolidColorBrush(Colors.White);
            DataContext = this;
            Axis axisX = (Axis)LineGraph.AxisX[0];
            axisX.MaxValue = 12; // Set maximum value
            axisX.MinValue = 0;  // Set minimum value
            axisX.Separator.Step = 1; // Set step interval between ticks
            // Customize X-axis labels
            LineGraph.AxisX.Clear();

            LineGraph.AxisX.Add(new Axis
            {
                Title = "Week",
                Labels = new[] { "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun" }

            });

            activities = checkBoxes.Where(c => c.IsChecked == true).Select(c => (ActivityType)c.Tag).ToArray();
            string outputList = activities.Length == 0 ? "Nothing" : string.Join(", ", activities);
            label.Content = $"You want to see these graph(s): {outputList}";

            //Ollie: Making sure the LG only shows the appropriate lines. I know it's poorly coding but I couldn't think of a simpler way rn
            if (outputList.Contains("Steps"))
            {
                StepsLine.Visibility = System.Windows.Visibility.Visible;
            }
            if (outputList.Contains("Water"))
            {
                WaterLine.Visibility = System.Windows.Visibility.Visible;
            }
            if (outputList.Contains("Sleep"))
            {
                SleepLine.Visibility = System.Windows.Visibility.Visible;
            }
            if (outputList.Contains("Work"))
            {
                WorkLine.Visibility = System.Windows.Visibility.Visible;
            }
            if (outputList == "Nothing")
            {
                LineGraph.Visibility = System.Windows.Visibility.Hidden;
            }
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
            if (cbi.Content.ToString() == "week")
            {
                LineGraph.AxisX.Clear();
                DataContext = this;
                // Customize X-axis labels
                LineGraph.AxisX.Add(new Axis
                {
                    Title = "Week",
                    Labels = new[] { "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun" }

                });
                Axis axisX = (Axis)LineGraph.AxisX[0];
                axisX.MaxValue = 6; // Set maximum value
                axisX.Separator.Step = 1;
            }
            else if (cbi.Content.ToString() == "month")
            {
                //month looks very janky atm due to size but what else can we actually do
                LineGraph.AxisX.Clear();
                DataContext = this;
                // Customize X-axis labels

                LineGraph.AxisX.Add(new Axis
                {
                    Title = "Month",

                });
                Axis axisX = (Axis)LineGraph.AxisX[0];
                axisX.MaxValue = 27; //this needs to be changed depending on the month
                axisX.Separator.Step = 1;
            }
            else if (cbi.Content.ToString() == "year")
            {
                LineGraph.AxisX.Clear();
                DataContext = this;
                // Customize X-axis labels

                LineGraph.AxisX.Add(new Axis
                {
                    Title = "Year",
                    Labels = new[] { "Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec" } // X-axis labels


                  });
                Axis axisX = (Axis)LineGraph.AxisX[0];
                axisX.MaxValue = 11; // Set maximum value
                axisX.Separator.Step = 1;
            }
            Trace.WriteLine(cbi.Content.ToString());
        }
    }

}
