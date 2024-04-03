using System.Windows;
using System.Windows.Controls;

namespace PI_Systems.GUIs
{
    /// <summary>
    /// Interaction logic for AchievementsPage.xaml
    /// </summary>
    public partial class AchievementsPage : Page
    {
        public AchievementsPage()
        {
            InitializeComponent();
        }

        private void ToMenuButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = MenuPage.instance;
        }
    }
}
