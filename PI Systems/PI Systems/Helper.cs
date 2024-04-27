namespace PI_Systems
{
    internal class Helper
    {
        public static int TimeFrameToDays(TimeFrame timeFrame)
        {
            return timeFrame switch
            {
                TimeFrame.Today => 1,
                TimeFrame.Week => 7,
                TimeFrame.Month => 30,
                _ => 1,
            };
        }

        public static string ActivityToUnit(ActivityType activityType)
        {
            return activityType switch
            {
                ActivityType.Steps => "step",
                ActivityType.Sleep => "hour",
                ActivityType.Water => "litre",
                ActivityType.Work => "hour",
                _ => "",
            };
        }
    }
}
