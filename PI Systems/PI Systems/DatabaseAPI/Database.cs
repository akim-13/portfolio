using PI_Systems.Properties;
using Microsoft.Data.SqlClient;
using System.Data;
using Dapper;
using System;
using System.Linq;
using System.Windows.Documents;
using System.Collections.Generic;
using System.Collections;

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


        private bool InsertWithQuery(string query, object newEntry)
        {
            try
            {
                conn.Execute(query, newEntry);
                return true;
            }
            // Jeet: If the insertion causes any issues, like primary key contraint breaking
            catch (SqlException)
            {
                Console.WriteLine("Insertionn error");
                return false;
            }
        }

        public bool Insert(UserActivity newEntry, string tableName)
        {
            return InsertWithQuery(
                $"INSERT INTO {tableName} (Username, Date, Value) VALUES (@Username, @Date, @Value)",
                newEntry);
        }

        public bool Insert(UserGoals newEntry)
        {
            return InsertWithQuery(
                "INSERT INTO UserGoals VALUES (@Username, @ActivityID, @TimeFrameID, @Date, @Value)",
                newEntry);
        }

        #endregion

        #region Updates

        bool UpdateWithQuery(string query, object entry)
        {
            try
            {
                conn.Execute(query, entry);
                return true;
            }
            catch
            {
                return false;
            }   
        }

        public bool Update(UserActivity entry, string tableName)
        {
            return UpdateWithQuery(
                $"UPDATE {tableName} SET Value = @Value WHERE Username = @Username AND Date = @Date",
                entry);
        }

        public bool Update(UserGoals entry)
        {
            return UpdateWithQuery(
                "UPDATE UserSteps SET TimeFrameID = @TimeFrameID, Date = @Date, Value = @Value WHERE Username = @Username AND Date = @Date",
                entry);
        }

        #endregion




        /// <summary>
        /// Gets the data from the one of the 3 user activities (water, sleep, steps).
        /// If one of the dates is not in the table, will add it to the array as a UserActivity object with the value set to default (0)
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="startDate"></param>
        /// <param name="endDate"></param>
        /// <returns></returns>
        public UserActivity[] GetUserActivities(DateTime startDate, DateTime endDate, string tableName)
        {
            string query = $"SELECT * FROM {tableName} WHERE Date >= @startDate AND Date <= @endDate";

            List<UserActivity> rows = conn.Query<UserActivity>(query, new { startDate, endDate }).ToList();

            // Go through all the days between these two dates (inclusive, which is why <= is used)
            for (int i = 0; i <= (endDate-startDate).Days; i++) 
            { 
                // Check whether the date is within the list, and if not add it to the list 
                DateTime date = startDate.AddDays(i);
                if (!rows.Select(x => x.Date).Contains(date))
                {
                    rows.Add(new UserActivity { Date = date });
                }
            }

            return rows.ToArray();

        }

        public UserActivity? GetUserActivityAt(DateTime startDate, string tableName)
        {
            // Jeet: typeof(T).Name gets the name of the class.
            // Since the class names are the same as the SQL table names, we can use them
            string query = $"SELECT * FROM {tableName} WHERE Date = @startDate";
            try
            {
                return conn.QueryFirst<UserActivity>(query, new { startDate });
            }
            catch (InvalidOperationException)  // Jeet: If this entry isn't in the db, return null (default)
            {
                return null;
            }
        }

        public string GetStringDataToday(string tableName)
        {
            object? item = GetUserActivityAt(DateTime.Now.Date, tableName);
            if (item != null)
            {
                return item.ToString();
            }
            return "0";
        }

        public UserGoals? GetUserGoal(string Username, int ActivityID)
        {
            string query = $"SELECT * FROM UserGoals WHERE Username = @Username AND ActivityID = @ActivityID";
            try
            {
                return conn.QueryFirst<UserGoals>(query, new { Username, ActivityID });
            }
            catch (InvalidOperationException)  // Jeet: If this entry isn't in the db, return null
            {
                return null;
            }
        }

        public void DeleteUserGoal(string Username, int ActivityID)
        {
            conn.Execute("DELETE FROM UserGoals WHERE Username = @Username AND ActivityID = @ActivityID", new { Username, ActivityID });
        }
    }
}
