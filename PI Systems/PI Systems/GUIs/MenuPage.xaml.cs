using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace PI_Systems.GUIs
{
    /// <summary>
    /// Interaction logic for MenuPage.xaml
    /// </summary>
    public partial class MenuPage : Page
    {
        public static MenuPage? instance;

        public MenuPage()
        {
            InitializeComponent();
            stepsCheckBox.Tag = ActivityType.Steps;
            sleepCheckBox.Tag = ActivityType.Sleep; 
            waterCheckBox.Tag = ActivityType.Water;
            workCheckBox.Tag = ActivityType.Work;
            instance = this;
        }

        private void SleepButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = new SleepPage();
        }

        private void StepsButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = new StepsPage();
        }

        private void WorkButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = new WorkPage();
        }

        private void WaterButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = new WaterPage();
        }

        private void GraphsButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = new GraphsPage(stepsCheckBox, sleepCheckBox, workCheckBox, waterCheckBox);
        }

        private void AchievementsButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = new AchievementsPage();
        }
    }
}
