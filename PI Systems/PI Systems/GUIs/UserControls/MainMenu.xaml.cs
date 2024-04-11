using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for Menu.xaml
    /// </summary>
    public partial class MainMenu : UserControl
    {
        public static MainMenu Instance { get; private set; }

        public string waterToday;
        public string sleepToday;
        public string stepsToday;

        public string user = "TestUser";

        public MainMenu()
        {
            InitializeComponent();
            Instance = this;

            // Jeet: The tag property of a xaml object can hold anything, so you can associate C# objects with these xaml items
            stepsCheckBox.Tag = ActivityType.Steps;
            sleepCheckBox.Tag = ActivityType.Sleep;
            waterCheckBox.Tag = ActivityType.Water;
            workCheckBox.Tag = ActivityType.Work;

            workButton.Tag = new Work();
            sleepButton.Tag = new Sleep();
            stepsButton.Tag = new Steps();
            waterButton.Tag = new Water();
            achievementsButton.Tag = new Achievements();

            RefreshTodaysData();
        }

        private void BaseActivityButton_Click(object sender, RoutedEventArgs e)
        {
            Button button = (Button)sender;
            if (button.Equals(graphsButton))
            {
                // Jeet: The graph needs the info from this UserController: what checkboxes have been pressed
                Application.Current.MainWindow.Content = new Graphs(stepsCheckBox, sleepCheckBox, workCheckBox, waterCheckBox);
            }
            else
            {
                // Jeet: The window content switches back to whatever UserController object was associated with the button tag
                Application.Current.MainWindow.Content = button.Tag;
            }
        }

        public void RefreshTodaysData()
        {
            sleepToday = Database.Instance.GetStringDataToday<UserSleep>();
            stepsToday = Database.Instance.GetStringDataToday<UserSteps>();
            waterToday = Database.Instance.GetStringDataToday<UserWater>();

            // Displaying amount of each activity done today
            sleepLabel.Content = sleepToday + " hours";
            stepsLabel.Content = stepsToday + " steps";
            waterLabel.Content = waterToday + " litres";
        }
    }
}
