r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""


# A class for the input grammar
class Grammar:
    # Init function for the class
    def __init__(self, P, NT, T):
        # Initialize all the attributes
        self.productions = P
        self.NT = NT
        self.T = T
        self.LRProductions = {}
        for _ in self.NT:
            self.LRProductions[_] = []

    # A function to test for left recursive grammar
    def leftRecursive(self):
        # Initialize the flag
        flag = False
        # For each production
        for i in self.productions:
            # Check if left recursive for element i
            flag, j = self.__LRRecursive(i, i)
            self.LRProductions[i].append(j)
        return flag

    # A private recursive function to test left or right recursion
    def __LRRecursive(self, it, i, visited=None):
        # If visited is null, initialize a list
        if visited is None:
            visited = []
        # Append the current visited variable
        visited.append(it)
        # Initialize flag and RHS set
        flag = False
        RHS = set()
        # For every production of it
        for j in self.productions[it]:
            # Create a set, to remove duplicates
            RHS |= set(j)
            # For left recursion, check the first element
            if i == j[0]:
                flag = True
                return flag, j
        # For every element in the RHS
        for j in RHS:
            # If the element is a non terminals and has not yet been visited
            if j in self.NT and j not in visited:
                # Recursive function call on j
                flag = self.__LRRecursive(j, i, visited)
        return flag, 0

    # A function to convert LR grammar to RR
    def convertLRtoRR(self):
        # Loop through all LR productions
        for _ in self.LRProductions:
            # Eliminate the LR productions
            self.__convertLRtoRR(_)

    # A private function to eliminate LR production of sym
    def __convertLRtoRR(self, sym):
        # For indirect LR dependencies
        # Loop through its non terminal LR productions
        for i in self.LRProductions[sym]:
            # Remove indirect LR productions
            if i != sym:
                # Loop through the transitions of symbol
                for j in range(len(self.productions[sym])):
                    # If i is the the start of the transition
                    if self.productions[sym][j][0] == i:
                        # Copy the RHS of the transition
                        RHS = self.productions[sym][j][1:]
                        # For every transition of i
                        for _ in self.productions[i]:
                            # If the sym is the start of the the transition
                            if sym == _[0]:
                                # Remove the current transition
                                self.productions[sym].pop(j)
                                # Add the modified transition
                                self.productions[sym].insert(j, _ + RHS)
        # Left recursion format ::
        # A -> A alpha1 | A alpha2 | A alpha3 | ... | beta1 | beta2 | beta3 | ...
        alpha = []
        beta = []
        # For direct LR dependencies
        for i in self.productions[sym]:
            # If the start symbol does not match, it is a beta
            if i[0] != sym:
                beta.append(i)
            # If the start symbol matches, it is an alpha
            else:
                alpha.append(i[1:])
        # Modify the above LR grammar to RR grammar by applying the rule
        # A -> beta1 A' | beta2 A' | beta3 A' | ...
        # A' -> alpha1 A' | alpha2 A' | alpha3 A' | ... | epsilon
        self.productions[sym] = []
        self.NT.append(sym + '\'')
        self.productions[sym + '\''] = []
        # Append the same for the each alpha
        for _ in alpha:
            self.productions[sym + '\''].append(_ + sym + '\'')
        # Append epsilon (here ~) to the production of sym'
        self.productions[sym + '\''].append('~')
        # Append the same for the each beta
        for _ in beta:
            self.productions[sym].append(_ + sym + '\'')
