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
        public static Database instance;

        readonly SqlConnection conn;

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

            instance = this;
        }

        #region Insertions

        public bool InsertUserWater(UserWater newEntry)
        {
            try
            {
                string query = "INSERT INTO UserWater VALUES (@Username, @Date, @LitresDrank)";
                conn.Execute(query, newEntry);
                return true;
            }
            // Jeet: If the insertion causes any issues, like primary key contraint breaking
            catch (SqlException)
            {
                return false;
            }
        }

        public bool InsertUserSleep(UserSleep newEntry)
        {
            try
            {
                string query = "INSERT INTO UserSleep VALUES (@Username, @Date, @SleepHours)";
                conn.Execute(query, newEntry);
                return true;
            }
            catch (SqlException)
            {
                return false;
            }
        }

        #endregion

        #region Updates

        public void UpdateUserWater(UserWater newEntry)
        {
            string query = "UPDATE UserWater SET LitresDrank = @LitresDrank " +
                "WHERE Username = @Username AND Date = @Date";
            conn.Execute(query, newEntry);
        }

        public void UpdateUserSleep(UserSleep newEntry)
        {
            string query = "UPDATE UserSleep SET LitresDrank = @SleepHours " +
                "WHERE Username = @Username AND Date = @Date";
            conn.Execute(query, newEntry);
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
            string query = "SELECT * FROM UserWater WHERE Date >= @startDate AND Date <= @endDate";

            return conn.Query<T>(query, new { startDate, endDate }).ToArray();
        }

        public T? GetUserActivity<T>(DateTime startDate)
        {
            string query = "SELECT * FROM UserWater WHERE Date = @startDate";
            try
            {
                return conn.QueryFirst<T>(query, new { startDate });
            }
            catch (InvalidOperationException)  // Jeet: If this entry isn't in the db, return null (default)
            {
                return default;
            }
        }

    }
}
