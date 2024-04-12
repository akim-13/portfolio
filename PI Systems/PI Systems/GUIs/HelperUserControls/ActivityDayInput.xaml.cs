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
                    UpdateUserSleep();
                    break;
                case ActivityType.Steps:
                    UpdateUserSteps();
                    break;
                case ActivityType.Work:
                    break;
            }
            MainMenu.Instance.RefreshTodaysData();
            //((GoalAndDailyInput)Tag).goalInput.DisplayGoal();
        }

        

        #region Update Various Different Activity Types

        private void InsertOrUpdate(dynamic entry)
        {
            // Jeet: Try inserting data, and if it can't be inserted (since it already exists), update it 
            if (!Database.Instance.Insert(entry))
            {
                Database.Instance.Update(entry);
            }
        }

        void UpdateUserWater()
        {
            UserWater entry = new UserWater
            {
                Username = MainMenu.Instance.user,
                Date = DateTime.Now.Date,
                LitresDrank = float.Parse(textBox.Text)
            };
            InsertOrUpdate(entry);
        }

        void UpdateUserSleep()
        {
            UserSleep entry = new UserSleep
            {
                Username = MainMenu.Instance.user,
                Date = DateTime.Now.Date,
                SleepHours = float.Parse(textBox.Text)
            };
            InsertOrUpdate(entry);
        }

        void UpdateUserSteps()
        {
            UserSteps entry = new UserSteps
            {
                Username = MainMenu.Instance.user,
                Date = DateTime.Now.Date,
                Steps = int.Parse(textBox.Text)
            };
            InsertOrUpdate(entry);
        }

        #endregion

        #region Constraining Textbox Input 

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
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