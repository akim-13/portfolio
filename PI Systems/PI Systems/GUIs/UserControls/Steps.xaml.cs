using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
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
    /// Interaction logic for Steps.xaml
    /// </summary>
    public partial class Steps : UserControl
    {
        public Steps()
        {
            InitializeComponent();
        }

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {

        }

        private void FitbitButton_Click(object sender, RoutedEventArgs e)
        {
            Trace.WriteLine("Send to FitBit Auth");
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
