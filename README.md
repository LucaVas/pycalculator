# PYCALC
#### Video Demo: <https://youtu.be/Pu0oIyOsHEI>
#### Description:
1-13: import of libraries
15-19: setting of constants color pallette
21: declaring an empty list where the calculation history will be stored

24-81: declaring the class InitWindow which will generate a new window. 
    35-47: The window will appear center screen, with title and icon
    49-61: The window will have a label with welcome text and the layout will be set as grid
    63-81: The window will have 2 buttons, blue and grey, to decide the mode of your interface (dark/light)

84-131: declarting the class Button which will be used to generate buttons in the whole app
    93-131: style option which will be applied to the button depending on the variable entered as argument of the class

134-169: declaring the class Label which is used to generate the label of the calculator
    135-169: styling the label, that it would change color depending on the mode and would have text displayed central and left-side

172-602: declaring the class Calculator which will be our specific app
    172-199: setting style to widget depending on the mode chosen, adding title, icons, calling history() variable to store the history of calculation, creating a list of errors (for now 1) to call in case of wrong calculation;
    201-338: setting grid layout to the calculator, and adding buttons to each row and column; afterwards connecting them to methods in the class, depending on the button chosen
    340-377: method which interacts with keyboard, identifies the key pressed and calls a method depending on the key text
    379-382: method which identifies center of screen, and let the widget be placed there
    384-389: methods which delete 1 digit at time or delete the entire text when called by DEL or CE buttons
    391-427: method which identifies the button pressed, then perform a calculation or add digits depending on the regex and other rules
    429-456: methods which multipy by 100 or add floating point if percentage or float buttons are pressed
    458-478: method which performs calculation, display the result and add the calculation to the history() variable
    580-602: methods which change sign of the number displayed and time at 1000ms the duration of the error displayed

605-622: main function()
    625-636: method which initiate the application
    639-653: method which generates Excel file with calculation history (upon request)
    656-667: method which displays in terminal the calculation history (upon request)

670-671: calling the main() function if file is main

#### Mode of use:
pyCalc is a calculator app developed in Python using a GUI developed with PyQt5 third-party library.
Important: The application must be executed by adding " -exe " as second argument of terminal line (i.e., 'python ./project.py -exe').
Once the application is initialized, you can choose between dark and light mode. 
Each calculation can have no more or less than 2 arguments and one operator. If you would try to add another operator/argument, the application would immediately perform the calculation of what is already present in the label.
If you divide by 0, the application will display an error message for 1000 ms.
You can calculate with positive and negative numbers, floats and integers. 
If the digits length would exceed that of the calculator, it will automatically expand to fit the digits until 400px. The minimum width is 300px.
At the end of the file, you can chose to export your history of calculation in a new Excel file.
Finally, you are asked if you wish to see the history in your terminal window.


#### History of the project:
During the planning phase, trying to decide what kind of project could summarize my CS50P journey, I decided to conduct more research about GUI environment in Python. 
With some experience in front-end web developement, I felt that CS50P gave me a lot in terms of back-end and data manipulation. Nevertheless, I felt that I missed the user experience given by a front-end app, and expecially the satisfaction given by seing your application take life.
Almost parallely, I understood that my understanding of OOP was still very fragile. I wanted to find a project where I could strengthen my knowledge in OOP, and especially in the use of classes.

After a short research, I understood that, between Pygame, Tkinter, and PyQt, the best library which could give me powerful GUI interface and widely used (so worth investing time in) would be PyQt5.
Initially I developed the graphical skeleton, trying to understand how to create a Widget, how to initialize the application, how to place buttons and labels in the widget. 
After creating the first graphical draft, I figured out that Widget could also host grids, which then I applied to the code (basically re-writing the part where I would place buttons manually in the Widget, and transferring them into a grid).

While reviewing my code, I felt that all parts of it where in one single class. This looked very messy and difficult to clean up or debug.
This is where I started dividing single parts of my app into classes, and then let them communicate with each other. This was overall an amazing experience in working with classes, inheritance, methods and attributes within.

Later came the longest part of the developement, i.e. debugging. I kind of underestimated the complexity of a single calculator, but I then understood how many edge cases there could be and how many different bugs can appear. For example:
1 - What if user enters an operator or a dot without any number?
2 - What if user enters a dot right before or after an operator?
3 - What if user wants to divide by 0?
4 - What if user divides with 0 remainder, or not, and how should the result appear? how many decimals after the floating point?
5 - How to display the result in the label while passing between floating and int calculations?
And much more

When the debugging was finalized, I realized that, according to CS50 guidelines, my application needed to have 3 sub functions in the main() function.
At that moment, my app didn't really need any. I decided to add a function which would ask the user for the dark/light mode he would like to use the calculator in. Later on, I realized that such function did not need to be in the main(), but inside the class itself, leaving me without solutions.

I then decided to integrate another feature which would prompt the user for whether they want to export the history of their calculation in a separate Excel file, and whether then they would want to display the result in the terminal.
This allowed me to work on CSV and file I/O, a very interesting topic throughout the CS50P course.

Finally, I wanted to add a last touch to the app and make sure that the user could imput digits and operators also with his keyboard, which is usually the way I prefer to use a calculator.
This really helped me understand better signals, events and overall keyboard-app relationship.

Overall, this app helped me strengthen my knowledge in OOP and GUI Python, and allowed me to develop an everyday user-end application which could be useful in everyday life.