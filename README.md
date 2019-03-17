Texas holdem Poker Hand Solver.
================================

Currently this program can be run two different ways:
Executing the GUI
Through an IDE or python's command line


Method 1, Graphical User Interface:
====================================

To run this program with the gui, download: 
DebugTests.py, solvepokerhands.py, table.py, Probability/Probability.py, PokerUserInterface/pokerUI
be sure to also download the __init__ files in each folder

install python 3.4 (inside of root dir)
install pyqt 4.11 (inside of PokerUserInterface folder)

Run pokerUI

A hand must have two cards to be played. Currently requires a flop as well.
Follow the error msg's if the program does not run.



Method 2, Cout statements:
===========================

To run this program with an IDE or command line, download: 
main.py, solvepokerhands.py, currentHand.py, table.py and Probability/Probability.py
be sure to also download the __init__ files in each folder

install python 3.4 (inside of root dir)

Run main.py

At the beginning of main, two variables can be modified.
The number of players can be anywhere from 2-10. Change the input of number of players to test it.
The number of cards shown can range from 3-5 (Flop-River). Change the input of number of community cards to test.



Method 3, Run EXE file:
========================

This is the best method I have been able to use thus far. Ideally, this will be put in a web browser.
Until then, you can simply download the texasHoldemPoker.exe in this directory, and run the file from your desktop.
I promise there is nothing malicious in the file.



Summary:
========

The program currently generates random hands for a various number of players, compares the 
hands against eachother, displays hands of similar strengths, then finally announces
the winning hand after breaking all ties.
-OR-
If the hand is not complete and has less than 5 community cards, it program will calculate
the odds of the hand winning. Then it displays each hand's chance of winning.



