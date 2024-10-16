﻿using System.Windows;
using System.Windows.Input;
using System;
using System.Windows.Controls;
using PI_Systems.GUIs.UserControls;

namespace PI_Systems.GUIs.HelperUserControls
{
    /// <summary>
    /// Interaction logic for ActivityDayInput.xaml
    /// </summary>
    public partial class ActivityDayInput : UserControl
    {
        public string? Prompt { get; set; }
        public ActivityType? Activity { get; set; }

        private float input;

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
            // James: Check for valid inputs before updating the activities
            if (!float.TryParse(textBox.Text, out input))
            {
                MessageBox.Show("This is not a valid input", "Invalid input", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            switch (Activity)
            {
                case ActivityType.Water:
                    // apparantly you die if you drink 6 litres of water in 3 hours, so capping at 48 should be safe enough
                    if (input <= 48) 
                    { 
                        UpdateUserWater(); 
                    }
                    else
                    {
                        MessageBox.Show("The max input is 48 litres", "Error Inputting", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                    break;
                case ActivityType.Sleep:
                    if (input <= 24) 
                    { 
                        UpdateUserSleep(); 
                    }
                    else
                    {
                        MessageBox.Show("The max input is 24hrs", "Error Inputting", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                    break;
                case ActivityType.Steps:
                    if (input <= 100000) 
                    { 
                        UpdateUserSteps(); 
                    }
                    else
                    {
                        MessageBox.Show("The max input is 100,000 steps", "Error Inputting", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                    break;
                case ActivityType.Work:
                    break;
            }
            MainMenu.Instance.RefreshTodaysData();
        }



        #region Update Various Different Activity Types

        private void InsertOrUpdate(UserActivity entry, string tableName)
        {
            // Jeet: Try inserting data, and if it can't be inserted (since it already exists), update it 
            if (!Database.Instance.Insert(entry, tableName))
            {
                Database.Instance.Update(entry, tableName);
            }
            updateButton.IsEnabled = false;
        }

        void UpdateUserWater()
        {
            UserActivity entry = new UserActivity
            {
                Username = MainMenu.Instance.user,
                Date = DateTime.Now.Date,
                Value = input
            };
            InsertOrUpdate(entry, "UserWater");
        }

        void UpdateUserSleep()
        {
            UserActivity entry = new UserActivity
            {
                Username = MainMenu.Instance.user,
                Date = DateTime.Now.Date,
                Value = input
            };
            InsertOrUpdate(entry, "UserSleep");
        }

        void UpdateUserSteps()
        {
            UserActivity entry = new UserActivity
            {
                Username = MainMenu.Instance.user,
                Date = DateTime.Now.Date,
                Value = input
            };
            InsertOrUpdate(entry, "UserSteps");
        }

        #endregion

        #region Constraining Textbox Input 

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (string.IsNullOrEmpty(textBox.Text))
            {
                // Jeet: If the user removes everything from the text box, set default to 0
                textBox.Text = "0";
                textBox.SelectAll();  // So that the user can easily overwrite the 0
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
            updateButton.IsEnabled = true;
            // Jeet: Set the data into the text box when this specific GUI component loads in on the screen
            switch (Activity)
            {
                case ActivityType.Water:
                    textBox.Text = MainMenu.Instance.waterToday;
                    break;
                case ActivityType.Sleep:
                    textBox.Text = MainMenu.Instance.sleepToday;
                    break;
                case ActivityType.Steps:
                    textBox.Text = MainMenu.Instance.stepsToday;
                    break;
            }
        }
    }
}
