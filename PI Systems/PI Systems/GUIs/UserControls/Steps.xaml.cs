using PI_Systems.DatabaseAPI;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;

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

        private async void FitbitButton_Click(object sender, RoutedEventArgs e)
        {
            FitbitAPI fitbit = new FitbitAPI(tokenTextBox.Text.Trim());
            await fitbit.FetchUserData();
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
