﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PI_Systems
{
    internal class Helper
    {
        public static int TimeFrameToDays(TimeFrame timeFrame)
        {
            return timeFrame switch
            {
                TimeFrame.Today => 1,
                TimeFrame.Week => 7,
                TimeFrame.Month => 30,
                _ => 1,
            };
        }
    }
}