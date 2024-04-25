using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for Achievements.xaml
    /// </summary>
    public partial class Achievements : UserControl
    {

        public int sleepAchievement;
        public int stepsAchievement;
        public int workAchievement;
        public int waterAchievement;

        public int achievementCounter = 0;

        public Achievements()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            UpdateSquareColor();
            UpdateCurrentStrike();
            UpdateWeekAchievements();
        }

        private void UpdateSquareColor()
        {
            bool condition2 = true;
            bool condition3 = true;
            bool condition4 = true;

            string getAchSleep;
            string getAchStep;
            string getAchWork;
            string getAchWater;

            string achievementMessage = "";

            // Katrya: gets sleep data
            getAchSleep = Database.Instance.GetStringDataToday("UserSleep");
            int achSleep = int.Parse(MainMenu.Instance.sleepToday);
            Console.WriteLine("Actual Sleep: " + achSleep.ToString());

            getAchStep = Database.Instance.GetStringDataToday("UserSteps");
            int achStep = int.Parse(getAchStep);

            getAchWater = Database.Instance.GetStringDataToday("UserWater");
            int achWater = int.Parse(getAchWater);

            getAchWork = Database.Instance.GetStringDataToday("UserWater");
            int achWork = int.Parse(getAchWork);


            if (achSleep > 8)
            {
                Achievement1.Fill = Brushes.GreenYellow;
                achievementCounter++;
                achievementMessage += "You slept enought hours today!\n";
            }
            else
            {
                achievementMessage += "You could've slept more today!\n";
            }
            if (achWork >= 2)
            {
                Achievement2.Fill = Brushes.GreenYellow;
                achievementCounter++;
                achievementMessage += "You worked for 2 hours today!\n";
            }
            else
            {
                achievementMessage += "You didn't manage to do much work today!\n";
            }
            if (achStep >= 60000)
            {
                Achievement3.Fill = Brushes.GreenYellow;
                achievementCounter++;
                achievementMessage += "You've completed steps goal for today!\n";
            }
            else
            {
                achievementMessage += "You can do more steps today!\n";
            }
            if (achWater >= 2)
            {
                Achievement4.Fill = Brushes.GreenYellow;
                achievementCounter++;
                achievementMessage += "You drank enough water today!\n";
            }
            else
            {
                achievementMessage += "Keep drinking more water!\n";
            }
            if (achievementCounter == 4)
            {
                achievementMessage = "Congratulations! \nYou have completed \nall the goals for today!";
            }
            printNote(achievementMessage);

        }

        private void UpdateCurrentStrike()
        {

        }

        private void UpdateWeekAchievements()
        {
            WeeklyAchievementsLabel.Content = achievementCounter + "/4";
        }
        public void printNote(string message)
        {
            motivationalNote.Content = message;
        }


    }
}
