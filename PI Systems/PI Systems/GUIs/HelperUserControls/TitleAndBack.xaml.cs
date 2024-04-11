using System.Windows;
using System.Windows.Controls;
using PI_Systems;

// This displays activity title and back button
namespace PI_Systems.GUIs.HelperUserControls
{
    /// <summary>
    /// Interaction logic for ActivityInfo.xaml
    /// </summary>
    public partial class TitleAndBack : UserControl
    {
        public string? Title { get; set; }

        public TitleAndBack()
        {
            InitializeComponent();
            DataContext = this;
        }


        private void ToMenuButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = UserControls.MainMenu.Instance;
        }
    }
}
