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

            Achievement1.Fill = Brushes.Gray;
            Achievement2.Fill = Brushes.Gray;
            Achievement3.Fill = Brushes.Gray;
            Achievement4.Fill = Brushes.Gray;

            achievementCounter = 0;
            if (achSleep >= 8)
            {
                Achievement1.Fill = Brushes.GreenYellow;
                achievementCounter++;
            }
            if (achWork >= 2)
            {
                Achievement2.Fill = Brushes.GreenYellow;
                achievementCounter++;
            }
            if (achStep >= 5000)
            {
                Achievement3.Fill = Brushes.GreenYellow;
                achievementCounter++;
            }
            if (achWater >= 2)
            {
                Achievement4.Fill = Brushes.GreenYellow;
                achievementCounter++;
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

            float totalSleep = Database.Instance.sumOfData("UserSleep");
            float totalWork = Database.Instance.sumOfData("UserWork");
            int totalSteps = Database.Instance.sumOfData("UserSteps");
            float totalWater = Database.Instance.sumOfData("UserWater");


            achievementMessage += $"You slept for {totalSleep} hours in total!\n";
            achievementMessage += $"You worked for {totalWork} hours in total.\n";
            achievementMessage += $"You've taken {totalSteps} steps\nin total!\n";
            achievementMessage += $"You drank {totalWater} litres\nof water in total!\n";

            printNote(achievementMessage);

        }

        private void UpdateCurrentStreak()
        {
            currentStreakLabel.Content = currentStreak + " days";
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