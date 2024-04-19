using System;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;

namespace PI_Systems.GUIs.HelperUserControls
{
    /// <summary>
    /// Interaction logic for WorkItem.xaml
    /// </summary>
    public partial class WorkItem : UserControl
    {
        public string? Title { get; set; }
        public string? Timer { get; set; }
        public int position { get; set; }
        public ControlState currState = ControlState.Paused;
        public DispatcherTimer dispatcherTimer = new DispatcherTimer();
        public Stopwatch stopwatch = new Stopwatch();

        // James: Handling killing this instance when ended
        public event EventHandler<string> KillCurrentWork;

        public WorkItem()
        {
            InitializeComponent();
            DataContext = this;
            controls_btn.Content = GetCurrentStateSymbol();
            dispatcherTimer.Tick += new System.EventHandler(dt_Tick);
            dispatcherTimer.Interval = new System.TimeSpan(0, 0, 0, 0, 1);

        }

        private void dt_Tick(object sender, System.EventArgs e)
        {
            if (currState == ControlState.Running)
            {
                TimeSpan ts = stopwatch.Elapsed;
                Timer = String.Format("{0:00}:{1:00}", ts.Minutes, ts.Seconds);
                timer.Content = Timer;
            }
        }

        private void ControlButton_Click(object sender, RoutedEventArgs e)
        {
            if (currState == ControlState.Paused)
            {
                currState = ControlState.Running;
                // James: Start the timer and stopwatch
                stopwatch.Start();
                dispatcherTimer.Start();
            }
            else
            {
                currState = ControlState.Paused;
                // James: Pause the timer and stopwatch
                stopwatch.Stop();
                dispatcherTimer.Stop();
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

        private void StopButton_Click(object sender, RoutedEventArgs e)
        {
            currState = ControlState.Ended;
            stopwatch.Stop();
            dispatcherTimer.Stop();
            KillCurrentWork?.Invoke(this, "");
        }
    }
}
