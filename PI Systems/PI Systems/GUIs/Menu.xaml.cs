using System;
using System.Windows;


namespace PI_Systems
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class Menu : Window
    {
        public Menu()
        {
            InitializeComponent();            
        }

        // This function will be called whenever the user clicks the button on the screen.
        // You can assign which function is triggered when a button is pressed in the xaml file. 
        private void TestButton_Click(object sender, RoutedEventArgs e)
        {     
            if (testText.IsVisible)
            {
                // If testText is visible, collapse it
                testText.Visibility = Visibility.Collapsed;
            }
            else
            {
                // Otherwise enable it
                testText.Visibility = Visibility.Visible;
            }
        }
    }
}
