using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Printing;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for Work.xaml
    /// </summary>
    public partial class Work : UserControl
    {
        const int MAX_ITEMS = 9;
        int currCol, currRow, currItem;
        bool reachedMaxItems;
        public Work()
        {
            InitializeComponent();

            currCol = 0;
            currRow = 0;
            currItem = 1;
            reachedMaxItems = false;
        }

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {

        }

        private void NewWorkButton_Click(object sender, RoutedEventArgs e)
        {
            if (!reachedMaxItems)
            {
                Trace.WriteLine("Added new work");
                // Create new WorkItem
                WorkItem wi = new WorkItem();
                // Set WorkItem's title and timer
                wi.Title = "Test " + currItem;
                wi.Timer = "00:00:00";

                // add new WorkItem to the grid
                Grid.SetColumn(wi, currCol);
                Grid.SetRow(wi, currRow);
                IncrementColAndRow();

                // add as children
                work_item_panel.Children.Add(wi);
            }
        }

        private void IncrementColAndRow()
        {
            if(currItem == MAX_ITEMS)
            {
                reachedMaxItems = true;
                return;
            }

            currCol = currCol < 2 ? currCol + 1 : currCol = 0;
            if(currCol == 0)
            {
                currRow++;
            }
            currItem++;
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
            Trace.WriteLine(cbi.Content.ToString());
        }

        private void new_work_btn_Click(object sender, RoutedEventArgs e)
        {

        }
    }
}
