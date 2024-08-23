using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Web;

class fitbitAPI
{
    static async Task Main(string[] args)
    {
        //****THESE WILL NEED TO BE CHANGED FOR YOUR USE****
        //At current will pull my (Tom's) data. Please don't steal my social security number :)
        //See fitbit website to register application - https://dev.fitbit.com/ -> manage -> register an app
        string clientId = "23S2MN";
        string redirectUri = "http://localhost";
        //****THESE WILL NEED TO BE CHANGED FOR YOUR USE****

        //Generate Code Verifier and Code Challenge used in API query
        string codeVerifier = GenerateCodeVerifier();
        string codeChallenge = GenerateCodeChallenge(codeVerifier);

        //Request Authorization to Fitbit User Data, it's the way fitbit requires it to be done
        string authoriseUrl = $"https://www.fitbit.com/oauth2/authorize?client_id={clientId}&response_type=code&code_challenge={HttpUtility.UrlEncode(codeChallenge)}&code_challenge_method=S256&redirect_uri={HttpUtility.UrlEncode(redirectUri)}&scope=activity%20heartrate%20location%20nutrition%20oxygen_saturation%20profile%20respiratory_rate%20settings%20sleep%20social%20temperature%20weight";

        //Prompts the user to go to verification page
        Console.WriteLine("Please visit the following URL in your browser to authorise the app:");
        Console.WriteLine(authoriseUrl);

        //Asks the user to enter the redirect they were taken to in order to obtain code
        Console.WriteLine("After authorisation, paste the redirected URL here:");
        string redirectedUrl = Console.ReadLine();

        //Retrieve authorisation code
        var queryString = new Uri(redirectedUrl).Query;
        var queryParameters = HttpUtility.ParseQueryString(queryString);
        string authorisationCode = queryParameters.Get("code");

        //Exchange Authorisation Code for Access and Refresh Tokens
        string accessToken = await GetAccessToken(clientId, authorisationCode, codeVerifier);

        if (!string.IsNullOrEmpty(accessToken))
        {
            //Prints all data relating to the user, warning this doesn't look very nice
            await FetchUserData(accessToken);
        }
        else //Something went wrong :(
        {
            Console.WriteLine("Failed to obtain access token.");
        }
    }

    static string GenerateCodeVerifier()
    {
        using (var rng = RandomNumberGenerator.Create())
        {
            byte[] bytes = new byte[32];
            rng.GetBytes(bytes);
            return Base64UrlEncode(bytes);
        }
    }

    static string GenerateCodeChallenge(string codeVerifier)
    {
        using (var sha256 = SHA256.Create())
        {
            byte[] bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(codeVerifier));
            return Base64UrlEncode(bytes);
        }
    }

    static async Task<string> GetAccessToken(string clientId, string authorisationCode, string codeVerifier)
    {
        string tokenUrl = "https://api.fitbit.com/oauth2/token";

        using (var httpClient = new HttpClient())
        {
            //Setting parameters to obtain access token
            var content = new FormUrlEncodedContent(new[]
            {
                new KeyValuePair<string, string>("client_id", clientId),
                new KeyValuePair<string, string>("code", authorisationCode),
                new KeyValuePair<string, string>("code_verifier", codeVerifier),
                new KeyValuePair<string, string>("grant_type", "authorization_code"),
                new KeyValuePair<string, string>("redirect_uri", "http://localhost")
            });

            var response = await httpClient.PostAsync(tokenUrl, content);

            if (response.IsSuccessStatusCode)
            {
                //Returns access token if connection is successful
                var responseContent = await response.Content.ReadAsStringAsync();
                dynamic responseData = Newtonsoft.Json.JsonConvert.DeserializeObject(responseContent);
                return responseData.access_token;
            }
            else
            {
                //For debugging, returns reason why connection failed
                Console.WriteLine($"Failed to get access token: {response.StatusCode} - {response.ReasonPhrase}");
                return null;
            }
        }
    }

    //Gets all user data - currently configured for steps and sleep
    static async Task FetchUserData(string accessToken)
    {
        string sleepUrl = "https://api.fitbit.com/1.2/user/-/sleep/date/today.json";
        string stepUrl = "https://api.fitbit.com/1/user/-/activities/date/today.json";

        using (var httpClient = new HttpClient())
        {
            //Fetch sleep data
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);
            var sleepResponse = await httpClient.GetAsync(sleepUrl);

            if (sleepResponse.IsSuccessStatusCode)
            {
                var sleepData = await sleepResponse.Content.ReadAsStringAsync();
                Console.WriteLine("Sleep Data:");
                Console.WriteLine(sleepData);
            }
            else
            {
                Console.WriteLine($"Failed to fetch sleep data: {sleepResponse.StatusCode} - {sleepResponse.ReasonPhrase}");
            }

            //Fetch step count data
            var stepResponse = await httpClient.GetAsync(stepUrl);

            if (stepResponse.IsSuccessStatusCode)
            {
                var stepData = await stepResponse.Content.ReadAsStringAsync();
                Console.WriteLine("Step Count Data:");
                Console.WriteLine(stepData);
            }
            else
            {
                Console.WriteLine($"Failed to fetch step count data: {stepResponse.StatusCode} - {stepResponse.ReasonPhrase}");
            }
        }
    }

    //Encoding used in code verifier and challenge
    static string Base64UrlEncode(byte[] bytes)
    {
        string base64 = Convert.ToBase64String(bytes);
        return base64.Replace('+', '-').Replace('/', '_').TrimEnd('=');
    }
}