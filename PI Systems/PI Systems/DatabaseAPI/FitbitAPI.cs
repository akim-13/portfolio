using System;
using System.Threading.Tasks;
using System.Net.Http.Headers;
using System.Net.Http;
using System.Text.Json;
using System.Collections.Generic;
using System.Text.Json.Serialization;

// eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1MzQ1oiLCJzdWIiOiJDMjhKV1MiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJlY2cgcnNldCByb3h5IHJwcm8gcnNsZSByY2YgcmFjdCBycmVzIHJsb2MgcndlaSByaHIgcnRlbSIsImV4cCI6MTcxMzM4OTcwNiwiaWF0IjoxNzEzMzYwOTA2fQ.0a0X-4OMubBBGB8jmLtxooEcvUqHEZZ1Cg7tCJVOtng

namespace PI_Systems.DatabaseAPI
{
    class FitbitSteps
    {
        [JsonPropertyName("activities-tracker-steps")]
        public List<Dictionary<string, string>>? TrackerSteps { get; set; }
    }

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
            string stepUrl = "https://api.fitbit.com/1/user/-/activities/tracker/steps/date/2024-04-17/today.json";

            using HttpClient httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);

            //Fetch step count data
            HttpResponseMessage stepResponse = await httpClient.GetAsync(stepUrl);

            if (stepResponse.IsSuccessStatusCode)
            {
                string stepDataStr = await stepResponse.Content.ReadAsStringAsync();
                FitbitSteps stepData = JsonSerializer.Deserialize<FitbitSteps>(stepDataStr);
                Console.WriteLine("Step Count Data:");
                stepData.TrackerSteps[0].TryGetValue("dateTime", out string value);
                Console.WriteLine(value);
                return;
            }



            Console.WriteLine($"Failed to fetch step count data: {stepResponse.StatusCode} - {stepResponse.ReasonPhrase}");
            
        }
    }
}
