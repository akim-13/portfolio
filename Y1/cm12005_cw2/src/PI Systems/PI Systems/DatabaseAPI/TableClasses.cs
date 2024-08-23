using System;

namespace PI_Systems
{
    // Jeet: this is responsible for the 3 tables: UserSleep, UserWater, UserSteps
    class UserActivity
    {
        public DateTime Date { get; set; }
        public string? Username { get; set; } = null;
        public float Value { get; set; } = 0f;

        public override string ToString()
        {
            return Value.ToString();
        }
    }

    class UserGoals : UserActivity
    {
        public int ActivityID { get; set; }
        public int TimeFrameID { get; set; }
    }
}
