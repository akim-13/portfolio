using System;
using System.Threading.Tasks;
using System.Net.Http.Headers;
using System.Net.Http;

// eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1MzQ1oiLCJzdWIiOiJDMjhKV1MiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyY2YgcnNsZSIsImV4cCI6MTcxMzIxMjgxMCwiaWF0IjoxNzEzMTg0MDEwfQ.2vT-TmNBma3NIlRWGGOw-H_WdmtPvSHG030e4t8V0vg

namespace PI_Systems.DatabaseAPI
{
    class FitbitAPI
    {
        string accessToken;

        public FitbitAPI(string token) 
        {
            accessToken = token;
        }

        //Gets all user data - currently configured for steps and sleep
        public async Task FetchUserData()
        {
            string sleepUrl = "https://api.fitbit.com/1.2/user/-/sleep/date/today.json";
            string stepUrl = "https://api.fitbit.com/1/user/-/activities/tracker/steps/date/2017-06-06/today.json";

            using HttpClient httpClient = new HttpClient();
            //Fetch sleep data
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);
            HttpResponseMessage sleepResponse = await httpClient.GetAsync(sleepUrl);

            if (sleepResponse.IsSuccessStatusCode)
            {
                string sleepData = await sleepResponse.Content.ReadAsStringAsync();
                Console.WriteLine("Sleep Data:");
                Console.WriteLine(sleepData);
            }
            else
            {
                Console.WriteLine($"Failed to fetch sleep data: {sleepResponse.StatusCode} - {sleepResponse.ReasonPhrase}");
            }

            //Fetch step count data
            HttpResponseMessage stepResponse = await httpClient.GetAsync(stepUrl);

            if (stepResponse.IsSuccessStatusCode)
            {
                string stepData = await stepResponse.Content.ReadAsStringAsync();
                Console.WriteLine("Step Count Data:");
                Console.WriteLine(stepData);
            }
            else
            {
                Console.WriteLine($"Failed to fetch step count data: {stepResponse.StatusCode} - {stepResponse.ReasonPhrase}");
            }
        }
    }
}
