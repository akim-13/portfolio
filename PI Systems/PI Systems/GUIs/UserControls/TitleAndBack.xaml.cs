using System.Windows;
using System.Windows.Controls;


// This displays activity title and back button
namespace PI_Systems.GUIs.UserControls
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
            Application.Current.MainWindow.Content = Menu.Instance;
        }
    }
}
