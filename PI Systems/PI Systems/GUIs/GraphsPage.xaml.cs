using System.Linq;
using System.Windows;
using System.Windows.Controls;


namespace PI_Systems.GUIs
{
    /// <summary>
    /// Interaction logic for GraphsPage.xaml
    /// </summary>
    public partial class GraphsPage : Page
    {
        ActivityType[] activities;

        public GraphsPage(params CheckBox[] checkBoxes)
        {
            InitializeComponent();

            activities = checkBoxes.Where(c => c.IsChecked == true).Select(c => (ActivityType)c.Tag).ToArray();
            string outputList = activities.Length == 0 ? "Nothing" : string.Join(", ", activities);
            label.Content = $"You want to see these graph(s): {outputList}";
        }

        private void ToMenuButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = MenuPage.instance;
        }
    }
}

public enum ActivityType
{
    Sleep,
    Steps,
    Work,
    Water
}