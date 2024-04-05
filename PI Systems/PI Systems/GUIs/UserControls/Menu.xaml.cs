using System.Windows;
using System.Windows.Controls;

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for Menu.xaml
    /// </summary>
    public partial class Menu : UserControl
    {
        public static Menu? Instance { get; private set; }

        public Menu()
        {
            InitializeComponent();

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

            Instance = this;
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
    }
}
