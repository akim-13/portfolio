using System;

namespace PI_Systems
{
    class UserWater
    {
        public string? Username { get; set; }
        public DateTime Date {  get; set; }
        public float LitresDrank { get; set; }
    }

    class UserSleep
    {
        public string? Username { get; set; }
        public DateTime Date { get; set; }
        public float SleepHours { get; set; }
    }
}
