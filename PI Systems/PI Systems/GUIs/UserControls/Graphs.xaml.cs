using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Controls;


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

            activities = checkBoxes.Where(c => c.IsChecked == true).Select(c => (ActivityType)c.Tag).ToArray();
            string outputList = activities.Length == 0 ? "Nothing" : string.Join(", ", activities);
            label.Content = $"You want to see these graph(s): {outputList}";
        }
    }
}
