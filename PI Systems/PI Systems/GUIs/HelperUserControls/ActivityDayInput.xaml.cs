using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System;

namespace PI_Systems.GUIs.HelperUserControls
{
    /// <summary>
    /// Interaction logic for ActivityDayInput.xaml
    /// </summary>
    public partial class ActivityDayInput : UserControl
    {
        public string? Prompt { get; set; }
        public ActivityType? Activity { get; set; }

        public ActivityDayInput()
        {
            InitializeComponent();

            // Jeet: Remember to do this, otherwise the properties won't be in xaml file (Prompt and Activity)
            DataContext = this;
            
            textBox.Text = "0";
        }

        private void UpdateButton_Click(object sender, RoutedEventArgs e)
        {
            // Jeet: Updates the inputted data to the database (depends on the Activity)
            switch (Activity)
            {
                case ActivityType.Water: 
                    UpdateUserWater();
                    break;
                case ActivityType.Sleep:
                    break;
                case ActivityType.Steps:
                    break;
                case ActivityType.Work:
                    break;
            }
        }

        

        #region Update Various Different Activity Types

        void UpdateUserWater()
        {
            UserWater newEntry = new UserWater
            {
                Username = "TestUser",
                Date = DateTime.Now.Date,
                LitresDrank = float.Parse(textBox.Text)
            };

            // Jeet: Try inserting data, and if it can't be inserted (since it already exists), update it 
            if (!Database.instance.InsertUserWater(newEntry))
            {
                Database.instance.UpdateUserWater(newEntry);
            }
        }

        #endregion

        #region Constraining Textbox Input 

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            TextBox textBox = (TextBox)sender;
            if (string.IsNullOrEmpty(textBox.Text))
            {
                // Jeet: If the user removes everything from the text box, set default to 0
                textBox.Text = "0";
                textBox.SelectAll(); // Selecting text so its easy for user to write over
            }
        }

        private void TextBox_PreviewTextInput(object sender, TextCompositionEventArgs e)
        {
            // Jeet: If we are working with the steps activity, we don't want user typing in floats (only ints)
            bool notValid;
            if (Activity == ActivityType.Steps)
            {
                notValid = !int.TryParse(textBox.Text + e.Text, out int _);
            }
            else
            {
                notValid = !float.TryParse(textBox.Text + e.Text, out float _);
            }

            if (notValid)
            {
                // Jeet: If this new text is not a float, mark as handled,
                // so it won't update the text
                e.Handled = true;
            }
        }

        private void TextBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                // Jeet: If user presses enter on the textbox we want it to loose focus.
                textBox.MoveFocus(new TraversalRequest(FocusNavigationDirection.Next));
            }
        }

        #endregion


        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            // Jeet: Set the data into the text box when this specific GUI component loads in on the screen
            switch (Activity)
            {
                case ActivityType.Water:
                    UserWater? water = Database.instance.GetUserActivity<UserWater>(DateTime.Now.Date);
                    if (water != null)
                    {
                        // Console.WriteLine("Setting water info");
                        textBox.Text = water.LitresDrank.ToString();
                    }
                    break;
                case ActivityType.Sleep:
                    UserSleep? sleep = Database.instance.GetUserActivity<UserSleep>(DateTime.Now.Date);
                    if (sleep != null)
                    {
                        textBox.Text = sleep.SleepHours.ToString();
                    }
                    break;
            }
        }
    }
}
