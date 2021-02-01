r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
from PyQt5.QtWidgets import QWidget, QGroupBox, QTextEdit, QVBoxLayout, QFormLayout, QLabel, QLineEdit


class MainWindow(QWidget):
    def __init__(self, grammar):
        super().__init__()
        self.grammar = grammar
        self.setWindowTitle("Convert LR grammar to RR grammar")
        self.hint = QLabel("Productions after converting the given left recursive grammar to right recursive grammar")
        # Creating a group box
        self.formGroupBox = QGroupBox("Grammar")
        # Creating a text edit for the productions
        self.productions = QTextEdit()
        self.productions.setReadOnly(True)
        # Creating a text edit for LR output
        self.LR = QLineEdit()
        # Set read only for the entries
        self.LR.setReadOnly(True)
        # Line text for terminals
        self.terminals = QLineEdit()
        # Set read only
        self.terminals.setReadOnly(True)
        # Line text for non terminals
        self.nonTerminals = QLineEdit()
        # Set read only
        self.nonTerminals.setReadOnly(True)
        # calling the method that create the form
        self.createForm()
        # creating a vertical layout
        mainLayout = QVBoxLayout()
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
        # setting lay out
        self.setLayout(mainLayout)
        self.grammar.convertLRtoRR()
        # Modify the UI values
        self.retranslateUI()

    # Create form method
    def createForm(self):
        # Creating a form layout
        layout = QFormLayout()
        # Adding rows
        # Output of terminals and non terminals of the grammar
        layout.addRow(QLabel("Non Terminals"), self.nonTerminals)
        layout.addRow(QLabel("Terminals"), self.terminals)
        layout.addRow(QLabel("Left Recursive"), self.LR)
        # Input of the productions and start symbol
        layout.addRow(self.hint)
        layout.addRow(QLabel("Productions"), self.productions)
        self.formGroupBox.setLayout(layout)

    # A function to update the outputs in the GUI
    def retranslateUI(self):
        # Convert the products dictionary to a string to set in the text box
        productions = ""
        # Loop through the non terminals
        for i in sorted(self.grammar.NT):
            RHS = ""
            # Get the transition of that terminals
            for j in self.grammar.productions[i]:
                RHS += j + " |"
            productions += i + " -> " + RHS[:-1] + '\n'
        productions = productions[:-1]
        # Set the values of terminals, non terminals and the modified productions
        self.terminals.setText(str(self.grammar.T))
        self.nonTerminals.setText(str(self.grammar.NT))
        self.LR.setText("Left Recursive")
        self.productions.setText(productions)
