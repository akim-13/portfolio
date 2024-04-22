using Microsoft.IdentityModel.Tokens;
using PI_Systems.DatabaseAPI;
using System;
using System.Diagnostics;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using Windows.ApplicationModel.UserActivities;

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
            UserActivity[]? dateSteps = await fitbit.FetchUserData(DateTime.Now.AddDays(-365).Date);
            if (dateSteps.IsNullOrEmpty())
            {
                MessageBox.Show("Something went wrong. Are you sure the token was correct?", "Error Connecting", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }
            dateSteps = dateSteps?.Where(x => x.Value != 0).ToArray();
            if (dateSteps.IsNullOrEmpty())
            {
                MessageBox.Show("Although the connection has been successful, no data has been added since you dont have any data about steps on your fitbit.", "Empty Data", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            foreach (UserActivity stepData in dateSteps)
            {
                Database.Instance.Insert(stepData, "UserSteps");
            }
            MessageBox.Show("Your fitbit data has been added to the database successfully :)", "Operation Successful", MessageBoxButton.OK, MessageBoxImage.Information);
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
