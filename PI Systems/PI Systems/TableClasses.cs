using System;

namespace PI_Systems
{
    class UserWater
    {
        public string? Username { get; set; }
        public DateTime Date {  get; set; }
        public float LitresDrank { get; set; }

        public override string ToString()
        {
            return LitresDrank.ToString();
        }
    }

    class UserSleep
    {
        public string? Username { get; set; }
        public DateTime Date { get; set; }
        public float SleepHours { get; set; }

        public override string ToString()
        {
            return SleepHours.ToString();
        }
    }

    class UserSteps
    {
        public string? Username { get; set; }
        public DateTime Date { get; set; }
        public int Steps { get; set; }

        public override string ToString()
        {
            return Steps.ToString();
        }
    }
}
