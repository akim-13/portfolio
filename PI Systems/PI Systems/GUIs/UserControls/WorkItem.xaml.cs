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

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for WorkItem.xaml
    /// </summary>
    public partial class WorkItem : UserControl
    {
        public String? Title { get; set; }
        public String? Timer { get; set; }
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
