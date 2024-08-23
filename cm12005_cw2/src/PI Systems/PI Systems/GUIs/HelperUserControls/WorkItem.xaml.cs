using PI_Systems.GUIs.UserControls;
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
            dispatcherTimer.Tick += new EventHandler(dt_Tick);
            dispatcherTimer.Interval = new TimeSpan(0, 0, 0, 0, 1);

        }

        private void dt_Tick(object sender, EventArgs e)
        {
            if (currState == ControlState.Running)
            {
                TimeSpan ts = stopwatch.Elapsed;
                Timer = string.Format("{0:00}:{1:00}", ts.Minutes, ts.Seconds);
                timer.Content = Timer;
            }
        }

        private void ControlButton_Click(object sender, RoutedEventArgs e)
        {
            // Jeet: When the user wants to start the timer
            if (currState == ControlState.Paused)
            {
                currState = ControlState.Running;
                // James: Start the timer and stopwatch
                stopwatch.Start();
                dispatcherTimer.Start();
                
            }
            else
            {
                Console.WriteLine("Started");
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

        // Jeet: This removes the WorkItem from the grid and also adds the time to the database;
        private void StopButton_Click(object sender, RoutedEventArgs e)
        {
            TimeSpan ts = stopwatch.Elapsed;
            
            // Jeet: Calc the total number of hours as a float 
            float hours = (float)(ts.TotalHours + (ts.TotalMinutes/60) + (ts.TotalSeconds / 3600));
            
            // Jeet: Try inserting into the database.
            bool hasInserted = Database.Instance.Insert(new UserActivity
            {
                Date = DateTime.Now.Date,
                Username = MainMenu.Instance.user,
                Value = hours
            }, 
            "UserWork");

            // Jeet: If we can't insert it (ie there is already an entry for today), we just add this amount on
            if (!hasInserted)
            {
                float currentWorkHours = float.Parse(Database.Instance.GetStringDataToday("UserWork"));
                Database.Instance.Update(new UserActivity
                {
                    Date = DateTime.Now.Date,
                    Username = MainMenu.Instance.user,
                    Value = currentWorkHours + hours
                }, 
                "UserWork");
            }

            currState = ControlState.Ended;
            stopwatch.Stop();
            dispatcherTimer.Stop();
            KillCurrentWork?.Invoke(this, "");
        }
    }
}
