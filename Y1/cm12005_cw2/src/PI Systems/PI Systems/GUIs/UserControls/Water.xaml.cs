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

namespace PI_Systems.GUIs.UserControls
{
    /// <summary>
    /// Interaction logic for Water.xaml
    /// </summary>
    public partial class Water : UserControl
    {
        public Water()
        {
            InitializeComponent();
        }

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            TextBox txtbx = (TextBox)sender;  
            Console.WriteLine(txtbx.Text);
        }

        private void TitleAndBack_Loaded(object sender, RoutedEventArgs e)
        {

        }
    }
}
