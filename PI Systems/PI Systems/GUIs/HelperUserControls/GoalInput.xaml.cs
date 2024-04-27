using System.Windows.Controls;
using System.Windows.Input;
using System.Windows;
using PI_Systems.GUIs.UserControls;
using System;
using System.Linq;

namespace PI_Systems.GUIs.HelperUserControls
{
    /// <summary>
    /// Interaction logic for GoalInput.xaml
    /// </summary>
    public partial class GoalInput : UserControl
    {
        public string? Prompt { get; set; }
        public ActivityType Activity { get; set; }

        public GoalInput()
        {
            InitializeComponent();
            DataContext = this;
        }

        #region Textbox input constraints

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

        private void UpdateButton_Click(object sender, RoutedEventArgs e)
        {
            UserGoals entry = new UserGoals
            {
                Username = MainMenu.Instance.user,
                ActivityID = (int)Activity,
                TimeFrameID = goalTimeFrame.SelectedIndex,
                Date = DateTime.Now.Date,
                Value = float.Parse(textBox.Text)
            };

            // Jeet: Try inserting data, and if it can't be inserted (since it already exists), update it 
            if (!Database.Instance.Insert(entry))
            {
                Database.Instance.Update(entry);
            }

            DisplayGoal();
        }

        private void DisplayGoal()
        {
            UserGoals? goal = Database.Instance.GetUserGoal(MainMenu.Instance.user, (int)Activity);
            if (goal != null)
            {
                TimeFrame timeFrame = (TimeFrame)goal.TimeFrameID;
                int period = Helper.TimeFrameToDays(timeFrame);
                int currentDay = (int)(DateTime.Now.Date - goal.Date).TotalDays + 1;

                float currentValue = GetSumData(goal.Date);
                string thisWord = timeFrame != TimeFrame.Today ? "this " : "";

                // Jeet: If the goal is still in date, display the stats of it
                if (currentDay <= period)
                {
                    progressLabel.Content = $"Progress for goal {thisWord}{timeFrame}";
                    progressText.Text = $"{Activity}: {currentValue}/{goal.Value}\nDay: {currentDay}/{period}";
                }

                // Jeet: Otherwise, show whether the user has completed the goal or not
                else if (currentValue < goal.Value)
                {
                    progressLabel.Content = $"Goal not completed";
                    progressText.Text = $"You were {currentValue} {Helper.ActivityToUnit(Activity)}s away from {thisWord}{timeFrame}'s goal you set!";
                }
                else
                {
                    progressLabel.Content = $"Goal Completed!";
                    progressText.Text = $"Congratulations, you completed your goal of {goal.Value} {Helper.ActivityToUnit(Activity)}s within {thisWord}{timeFrame}";
                }


                preExistingGoal.Visibility = Visibility.Visible;
                inputStackPanel.Visibility = Visibility.Collapsed;
            }
        }

        private float GetSumData(DateTime start)
        {
            return Database.Instance.GetUserActivities(start, DateTime.Now.Date, "User" + Activity.ToString()).Sum(x => x.Value);
        }

        private void DeleteGoalButton_Click(object sender, RoutedEventArgs e)
        {
            MessageBoxResult result = MessageBox.Show("Are you sure you want to delete this goal?", "Confirmation", MessageBoxButton.YesNo, MessageBoxImage.Warning);
            if (result == MessageBoxResult.Yes)
            {
                Database.Instance.DeleteUserGoal(MainMenu.Instance.user, (int)Activity);
                preExistingGoal.Visibility = Visibility.Collapsed;
                inputStackPanel.Visibility = Visibility.Visible;
            }
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            DisplayGoal();
        }

        
    }
}
