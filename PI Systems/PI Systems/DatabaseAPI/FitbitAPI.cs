using System;
using System.Threading.Tasks;
using System.Net.Http.Headers;
using System.Net.Http;
using System.Text.Json;
using System.Collections.Generic;
using System.Text.Json.Serialization;
using PI_Systems.GUIs.UserControls;

// eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1MzQ1oiLCJzdWIiOiJDMjhKV1MiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJlY2cgcmNmIHJhY3QgcnNldCBycmVzIHJociBycHJvIHJudXQgcnRlbSByc2xlIiwiZXhwIjoxNzEzNjQ2NDQ5LCJpYXQiOjE3MTM2MTc2NDl9.fEghhak2wt-zObPvzC6sxLILmRP03HeZwfvzltnGK00

namespace PI_Systems.DatabaseAPI
{
    class FitbitSteps
    {
        [JsonPropertyName("activities-tracker-steps")]
        public List<Dictionary<string, string>>? TrackerSteps { get; set; }
    }

    class DateSteps
    {
        public DateTime Date {  get; set; }
        public int Steps { get; set; }

        public DateSteps(DateTime Date, int Steps)
        {
            this.Date = Date;
            this.Steps = Steps;
        }
    }

    class FitbitAPI
    {
        string accessToken;

        public FitbitAPI(string token) 
        {
            accessToken = token;
        }

        //Gets all user data - currently configured for steps and sleep
        public async Task<UserActivity[]?> FetchUserData(DateTime currentDate)
        {
            string stepUrl = $"https://api.fitbit.com/1/user/-/activities/tracker/steps/date/{currentDate.ToString("yyyy-MM-dd")}/today.json";

            using HttpClient httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);

            //Fetch step count data
            HttpResponseMessage stepResponse = await httpClient.GetAsync(stepUrl);

            if (stepResponse.IsSuccessStatusCode)
            {
                string stepDataStr = await stepResponse.Content.ReadAsStringAsync();
                Console.WriteLine("JSON: " + stepDataStr);
                FitbitSteps? stepData = JsonSerializer.Deserialize<FitbitSteps>(stepDataStr);
                if (stepData == null || stepData.TrackerSteps == null)
                {
                    return null;
                }

                List<UserActivity> steps = new List<UserActivity>();  
                for (int i = 0; i < stepData.TrackerSteps.Count; i++)
                {
                    bool s1 = stepData.TrackerSteps[i].TryGetValue("dateTime", out string dateStr);
                    bool s2 = stepData.TrackerSteps[i].TryGetValue("value", out string stepsStr);

                    if (!(s1 && s2))
                    {
                        Console.WriteLine("this is bad");
                        // return steps.ToArray();
                    }
                    else
                    {
                        steps.Add(new UserActivity
                        {
                            Date = DateTime.Parse(dateStr),
                            Username = MainMenu.Instance.user,
                            Value = int.Parse(stepsStr)
                        });
                    }
                }

                return steps.ToArray();
            }
            Console.WriteLine($"Failed to fetch step count data: {stepResponse.StatusCode} - {stepResponse.ReasonPhrase}");

            return null;
            
        }
    }
}
