using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using PI_Systems.GUIs.HelperUserControls;

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for Work.xaml
    /// </summary>
    public partial class Work : UserControl
    {
        const int MAX_ITEMS = 9;
        int currCol, currRow, currItem;
        public Work()
        {
            InitializeComponent();

            currCol = 0;
            currRow = 0;
            currItem = 1;
        }

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {

        }

        private void NewWorkButton_Click(object sender, RoutedEventArgs e)
        {
            if (currItem <= MAX_ITEMS && new_work_textbox.Text != "")
            {
                // Create new WorkItem
                WorkItem wi = new WorkItem();
                // Set WorkItem's title and timer
                wi.Title = new_work_textbox.Text;
                wi.Timer = "00:00";
                wi.position = currItem;

                // add new WorkItem to the grid
                Grid.SetColumn(wi, currCol);
                Grid.SetRow(wi, currRow);
                IncrementColAndRow();
                currItem++;

                // add as children
                work_item_panel.Children.Add(wi);

                // Clear textbox text
                new_work_textbox.Text = "";

                // Subscribe to the childs kill event
                wi.KillCurrentWork += KillWorkItem;
            }
        }

        private void KillWorkItem(object sender, string e)
        {
            WorkItem wi = (WorkItem)sender;
            // James: Remove the item
            work_item_panel.Children.Remove(wi);
            currCol = 0;
            currRow = 0;
            // if the currItem is > items position, shift others down
            if (currItem > wi.position)
            {
                int currItemIndex = 0;

                while (currItemIndex < work_item_panel.Children.Count)
                {
                    WorkItem item = (WorkItem)work_item_panel.Children[currItemIndex];
                    if (item.position > wi.position)
                    {
                        // shift the positioning if this item
                        Grid.SetColumn(item, currCol);
                        Grid.SetRow(item, currRow);
                    }
                    IncrementColAndRow();
                    currItemIndex++;
                }
            }
            currItem--;
        }

        private void new_work_textbox_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if(e.Key == Key.Enter)
            {
                NewWorkButton_Click(sender, e);
            }
        }

        private void IncrementColAndRow()
        {
            currCol = currCol < 2 ? currCol + 1 : 0;
            if (currCol == 0)
            {
                currRow++;
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
            Trace.WriteLine(cbi.Content.ToString());
        }
    }
}
