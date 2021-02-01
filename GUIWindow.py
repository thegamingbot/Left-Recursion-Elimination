r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
# Import the required libraries
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QTextEdit, QPushButton, QLineEdit, QVBoxLayout, QFormLayout
from PyQt5 import QtCore

from Grammar import Grammar


# Class for the GUI Window
class GUIWindow(QWidget):
    switch_window = QtCore.pyqtSignal(Grammar)

    # Init function for the class
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle("Convert LR grammar to RR grammar")
        self.hint = QLabel("Add the start symbol production in the first.\nUse -> for transition and ~ for epsilon "
                           "and | alternate move")
        # Creating a group box
        self.formGroupBox = QGroupBox("Grammar")
        # Creating a text edit for the productions
        self.productions = QTextEdit()
        # Create a button for running the functions
        self.button = QPushButton("Compute")
        # On click property of the button
        self.button.clicked.connect(self.getInfo)
        # Creating a text edit for LR output
        self.LR = QLineEdit()
        # Set read only for the entries
        self.LR.setReadOnly(True)
        # Create the form
        self.createForm()
        # Creating a vertical layout
        mainLayout = QVBoxLayout()
        # Adding the hint
        mainLayout.addWidget(self.hint)
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
        # setting lay out
        self.setLayout(mainLayout)

    # Create form method
    def createForm(self):
        # Creating a form layout
        layout = QFormLayout()
        # Adding rows
        # Input of the productions and start symbol
        layout.addRow(QLabel("Productions"), self.productions)
        # Button for compute
        layout.addRow(self.button)
        layout.addRow(QLabel("Left Recursive"), self.LR)
        # Setting layout
        self.formGroupBox.setLayout(layout)

    # Get information from the aforementioned form
    def getInfo(self):
        # Make a list of the productions
        productionsList = [y for y in (x.strip() for x in self.productions.toPlainText().splitlines()) if y]
        productionsDict = {}
        # Convert the productions to a dictionary
        # Key is the LSH
        # Value is the list of transitions
        for _ in productionsList:
            x = _.replace(" ", "").split("->")
            y = x[1].split("|")
            productionsDict[x[0]] = y
        NT = []
        T = []
        # Append the non terminals to the list
        for i in productionsDict:
            NT.append(i)
        # Append the terminals to the list
        for i in productionsDict:
            for j in productionsDict[i]:
                for k in j:
                    if k not in NT:
                        T.append(k)
        # Remove duplicates from non terminals and terminals
        NT = list(set(NT))
        T = list(set(T))
        # Initialize the Grammar class
        grammar = Grammar(productionsDict, NT, T)
        # If the given grammar is left recursive
        if grammar.leftRecursive():
            self.LR.setText("Left Recursive")
            # Emit a signal to go to the next window
            self.switch_window.emit(grammar)
        else:
            self.LR.setText("Not Left Recursive")
