﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace PI_Systems.GUIs
{
    /// <summary>
    /// Interaction logic for WaterPage.xaml
    /// </summary>
    public partial class WaterPage : Page
    {
        public WaterPage()
        {
            InitializeComponent();
        }

        private void ToMenuButton_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.MainWindow.Content = MenuPage.instance;
        }
    }
}
