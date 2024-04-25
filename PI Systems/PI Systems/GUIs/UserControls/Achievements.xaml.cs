using System;
using System.Windows;
using System.Windows.Automation;
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

        public int achievementCounter;
        public int currentStreak = 0;

        public Achievements()
        {
            InitializeComponent();
        }

        private void UserControl_Loader(object sender, RoutedEventArgs e)
        {
            UpdateSquareColor();
            UpdateCurrentStreak();
            UpdateWeekAchievements();
        }

        private void UpdateSquareColor()
        {
            string getAchSleep;
            string getAchStep;
            string getAchWork;
            string getAchWater;

            string achievementMessage = "";

            getAchSleep = Database.Instance.GetStringDataToday("UserSleep");
            float achSleep = float.Parse(getAchSleep);

            getAchStep = Database.Instance.GetStringDataToday("UserSteps");
            int achStep = int.Parse(getAchStep);

            getAchWater = Database.Instance.GetStringDataToday("UserWater");
            float achWater = float.Parse(getAchWater);

            getAchWork = Database.Instance.GetStringDataToday("UserWork");
            float achWork = float.Parse(getAchWork);
            Console.WriteLine(achWork);

            achievementCounter = 0;
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
                currentStreak++;
                achievementMessage = "Congratulations! \nYou have completed \nall the goals for today!";
            }
            else
            {
                currentStreak = 0;
            }
            printNote(achievementMessage);

        }

        private void UpdateCurrentStreak()
        {
            currentStreakLabel.Content = currentStreak;
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