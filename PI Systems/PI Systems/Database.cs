using PI_Systems.Properties;
using Microsoft.Data.SqlClient;
using System.Data;
using Dapper;
using System;
using System.Linq;

namespace PI_Systems
{
    internal class Database
    {
        public static Database Instance { get; private set; }

        private readonly SqlConnection conn;

        public Database()
        { 
            string connString = Settings.Default.ConnectionString;
            conn = new SqlConnection(connString);

            // Jeet: We open the connection so that we can
            // access the data from database
            if (conn.State != ConnectionState.Open)
            {
                conn.Open();
            }            

            Instance = this;
        }

        #region Insertions

        private bool InsertIntoTable(string query, object newEntry)
        {
            try
            {
                conn.Execute(query, newEntry);
                return true;
            }
            // Jeet: If the insertion causes any issues, like primary key contraint breaking
            catch (SqlException)
            {
                return false;
            }
        }

        public bool Insert(UserWater newEntry)
        {
            return InsertIntoTable(
                "INSERT INTO UserWater VALUES (@Username, @Date, @LitresDrank)",
                newEntry);
        }

        public bool Insert(UserSleep newEntry)
        {
            return InsertIntoTable(
                "INSERT INTO UserSleep VALUES (@Username, @Date, @SleepHours)",
                newEntry);
        }

        public bool Insert(UserSteps newEntry)
        {
            return InsertIntoTable(
                "INSERT INTO UserSteps VALUES (@Username, @Date, @Steps)",
                newEntry);
        }

        #endregion

        #region Updates

        void UpdateTable(string query, object entry)
        {
            conn.Execute(query, entry);
        }

        public void Update(UserWater entry)
        {
            UpdateTable(
                "UPDATE UserWater SET LitresDrank = @LitresDrank WHERE Username = @Username AND Date = @Date",
                entry);
        }

        public void Update(UserSleep entry)
        {
            UpdateTable(
                "UPDATE UserSleep SET SleepHours = @SleepHours WHERE Username = @Username AND Date = @Date",
                entry);
        }

        public void Update(UserSteps entry)
        {
            UpdateTable(
                "UPDATE UserSteps SET Steps = @Steps WHERE Username = @Username AND Date = @Date",
                entry);
        }

        #endregion


        /// <summary>
        /// Specify the table class you want, eg GetUserActivities<UserWater>(...)
        /// This aviods the use of multiple methods of similar functionality for eact activity
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="startDate"></param>
        /// <param name="endDate"></param>
        /// <returns></returns>
        public T[] GetUserActivities<T>(DateTime startDate, DateTime endDate)
        {
            string query = $"SELECT * FROM {typeof(T).Name} WHERE Date >= @startDate AND Date <= @endDate";

            return conn.Query<T>(query, new { startDate, endDate }).ToArray();
        }

        public T? GetUserActivity<T>(DateTime startDate)
        {
            // Jeet: typeof(T).Name gets the name of the class.
            // Since the class names are the same as the SQL table names, we can use them
            string query = $"SELECT * FROM {typeof(T).Name} WHERE Date = @startDate";
            try
            {
                return conn.QueryFirst<T>(query, new { startDate });
            }
            catch (InvalidOperationException)  // Jeet: If this entry isn't in the db, return null (default)
            {
                return default;
            }
        }

        public string GetStringDataToday<T>()
        {
            object? item = GetUserActivity<T>(DateTime.Now.Date);
            if (item != null)
            {
                Console.WriteLine("Data: " + item.ToString());
                return item.ToString();
            }
            return "0";
        }
    }
}
