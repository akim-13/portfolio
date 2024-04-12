using System.Windows.Controls;

namespace PI_Systems.GUIs.HelperUserControls
{
    /// <summary>
    /// Interaction logic for GoalAndDailyInput.xaml
    /// </summary>
    public partial class GoalAndDailyInput : UserControl
    {
        public string? InsertPrompt { get; set; }
        public string? GoalPrompt { get; set; }
        public ActivityType Activity {  get; set; }

        public GoalAndDailyInput()
        {
            InitializeComponent();
            DataContext = this;
        }
    }
}
