using System.Windows;
using System.Windows.Controls;

namespace PI_Systems.GUIs.HelperUserControls
{
    /// <summary>
    /// Interaction logic for WorkItem.xaml
    /// </summary>
    public partial class WorkItem : UserControl
    {
        public string? Title { get; set; }
        public string? Timer { get; set; }
        public ControlState currState = ControlState.Paused;

        public WorkItem()
        {
            InitializeComponent();
            DataContext = this;
            controls_btn.Content = GetCurrentStateSymbol();
        }

        private void ControlButton_Click(object sender, RoutedEventArgs e)
        {
            if(currState == ControlState.Paused)
            {
                currState = ControlState.Running;
            } else
            {
                currState = ControlState.Paused;
            }

            Button btn = (Button)sender;

            btn.Content = GetCurrentStateSymbol();
        }

        private string GetCurrentStateSymbol()
        {
            switch (currState)
            {
                case ControlState.Paused: return "▶️";
                case ControlState.Running: return "||";
                case ControlState.Ended: return "❌";
                default: return "";
            }
        }
    }
}
