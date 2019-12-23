infinity = 1000000
invalid_node = -1

class Node:
    previous = invalid_node
    distfromsource = infinity
    visited = False

class Dijkstra:

    def __init__(self):
        '''initialise class'''
        self.startnode = 0
        self.endnode = 0
        self.network = []
        self.network_populated = False
        self.nodetable = []
        self.nodetable_populated = False
        self.route = []     # this will hold the current path of the network
        self.route_populated = False
        self.currentnode = 0

    # ----- POPULATE NETWORK 2D LIST -----
    def populate_network(self, filename):
        ''' <--- the populate network method will be used to iterate through a (txt) file
        filled with the network which is written with comma separated values between
        each edge in the network ---> '''

        self.network_populated = False      # initially sets the network to "un-populated"

        try:
            file = open(filename, "r")      # opens the file specified in the method parameters
        except IOError:     # catches an error is the file does not exist
            print "Network file does not exist"
            return      # early return if network population fails
        for line in file:
            self.network.append(map(int, line.strip().split(',')))       # fills the network 2d list with comma seperated values using the split method

        self.network_populated = True       # the network will then get set to populated
        file.close

    # ----- POPULATE NODE TABLE -----
    def populate_node_table(self):
        ''' <--- the populate node table method will be used to set the populate the node table
        with the values presented in the network, this will then initialise the starting node so
        the algorithm can run'''

        self.nodetable = []     # initially clears the node table for it to be repopulated
        self.nodetable_populated = False        # initially sets the node table to unpopulated

        if not self.network_populated:      # checks if the network has contents first
            print "Network is empty"
            return

        for node in self.network:
            self.nodetable.append(Node())           # populates the node table with the amount of nodes in the network

        self.nodetable[self.startnode].distfromsource = 0       # sets the start node in the node table to have 0 for a distance
        self.nodetable[self.startnode].visited = True       # the start node is set to visited as this is where the algorithm will start
        self.nodetable_populated = True     # sets the node table to 'populated'


    def parse_route(self, filename):
        '''<--- Reads each character in the specified file and sets the start and end node to the correct positions --->'''
        try:
            with open(filename, 'r') as line:
                path = line.readline()      # reads each character from the file and stores it into a list
                self.startnode = ord(path[0]) - 65      # set the start node to the converted ASCII to int values
                self.endnode = ord(path[2]) - 65        # set the end node to the converted ASCII to int values
                self.route_populated = True     # route is now populated so this gets set to true
        except IOError:     # everything wrapped in a try block to check if the file exists
            print "Route file does not exist"
            self.route_populated = False        # route is not populated so this gets set to false

    def return_near_neighbour(self):
        '''<--- this method will return all of the nodes which have a weight of more than 0 and
        are unvisited to the current node in the network, this will be used to determine which
        nodes can be accessed next --->'''

        nearnodes = []
        for index, edge in enumerate(self.network[self.currentnode]):       # enumerate through the current node in the network
            if edge > 0 and not self.nodetable[index].visited:      # checks if the edge is possible to visit and it hasn't been visited yet
                nearnodes.append(index)     # if a valid node is found, it will be added to the list of available nodes
        return nearnodes        # returns the possible nodes connected to the current node

    def calculate_tentative(self):
        ''' <--- this method is used to calculate distances for each of the nodes without marking
        any of the nodes as visited, this is to determine the shortest distance in the network --->'''

        nearest_neighbours = self.return_near_neighbour()

        for neighboursindex in nearest_neighbours:      # cycles through the nearest neighbours
            tent_dist = self.nodetable[self.currentnode].distfromsource \
                        + self.network[self.currentnode][neighboursindex]   # the current tentative distance is set to the sum of the current nodes distance from source
                                                                                #  and the distance of one of the neighbours to the current node
            if tent_dist < self.nodetable[neighboursindex].distfromsource:  # if the current tentative distance is less than one of the neighbours distances from source
                self.nodetable[neighboursindex].distfromsource = tent_dist  # that distance will then be set to the tentative distance
                self.nodetable[neighboursindex].previous = self.currentnode # and connect its previous to the current node

    def determine_next_node(self):
        '''<--- this method will determine the next node with the shortest distance from source
         to travel down, this will only check for nodes which are unvisited and that have the
         shortest distance from source--->'''

        dist_compare = infinity     # initially set to infinity
        self.currentnode = invalid_node

        for index, node in enumerate(self.nodetable):   # this will iterate through the node table looking at all the nodes distance from source
            if (node.distfromsource < dist_compare) and node.visited is False:  # if the node has both the shortest distance and is unvisited, it will become the next node
                dist_compare = node.distfromsource      # keeps changing until the shortest distance is found
                self.currentnode = index    # sets the new current node to the new found shortest distance node

    def calculate_shortest_path(self):
        '''<--- this method will calculate the shortest path from the start node
        to the end node, this will call all of the relevent methods used before to
        determine what is the shortest path. --->'''

        self.populate_node_table()      # initially populates the node table
        self.currentnode = self.startnode       # and sets the current node to its start

        while self.currentnode is not self.endnode and self.currentnode is not invalid_node:    # while the current node is not at the end of the path and it is not an invalid node
            self.calculate_tentative()      # the tentative distance will be calculated through the network
            self.determine_next_node()      # and the next node will be determined for the path
            self.nodetable[self.currentnode].visited = True

    def return_shortest_path(self):
        '''<--- this method will be used to display the final shortest path of the network --->'''

        self.calculate_shortest_path()      # calculates the shortest path
        curnode = self.endnode      # initially starts a the end node to reverse back through the path
        while curnode is not self.startnode:        # will run until start node is reached (end of path)
            if curnode is invalid_node: # if the current node is invalid node, an empty path and distance will be returned
                return self.route, 0
            self.route.append(chr(curnode + 65))        # appends the next node in the shortest path to a list
            curnode = self.nodetable[curnode].previous      # and cycles to the next previous node in the path

        self.route.append(chr(self.startnode + 65))     # adds the starting node to the end of the list
        self.route.reverse()    # reverses the list as the list will be in reverse because it started at the end node

        distance = self.nodetable[self.endnode].distfromsource  # the end nodes distance from source will be the overall path distance
        print "Distance From Source: " + str(distance)
        return self.route, distance     # returns the required values

class MaxFlow(Dijkstra): #inherits from Dijkstra class
    def __init__(self):
        '''initialise class'''
        Dijkstra.__init__(self)
        self.original_network = []      # this will be used to hold a copy of the network

    def populate_network(self, filename):
        ''' <--- this method will be used to populate the network 2D list from the provided
        "network.txt" file, this will then need to create a copy for use in max flow --->'''

        Dijkstra.populate_network(self, filename)   # uses the Dijkstras populate network as no change will be needed for max flow
        self.original_network = [newlist[:] for newlist in self.network]    # uses slice to create a copy of the original network

    def return_near_neighbour(self):
        ''' this method will be used to return the next neighbour in the network,
        here I have called the Dijkstra's method as no changes are needed for max flow,
        the only difference being that I will be handling flow capacity/bottlenecks
        rather than edge weight'''

        nearnodes = []
        for index, edge in enumerate(self.network[self.currentnode]):       # enumerate through the current node in the network
            if edge > 0 and not self.nodetable[index].visited:      # checks if the edge is possible to visit and it hasn't been visited yet
                nearnodes.append(index)     # if a valid node is found, it will be added to the list of available nodes
        return nearnodes        # returns the possible nodes connected to the current node

    def return_bottleneck_flow(self):
        '''<--- this method will be used to cycle through the shortest path presented
        and find the bottleneck value in the path (the flow capacity which is at its lowest,
        this will determine the maximum flow that can be put through this network path)  --->'''

        bottleneck = 0  # initially the bottleneck is set to 0 so if there is no path found, the bottleneck returned would be 0
        for index, node in enumerate(self.route):   # for loop to cycle through the shortest path
            if (index + 1) != len(self.route):    # checks if end of path
                if bottleneck == 0: # this will now set the bottleneck to infinity if this is a new path, allowing for the initial bottleneck to be set
                    bottleneck = infinity
                cur_node_path = (ord(self.route[index]) - 65) # assigns the current node in the path to a variable
                next_node_path = (ord(self.route[index + 1]) - 65)    # assigns the next node in the path to a variable
                flow = self.network[cur_node_path][next_node_path]  # assigns the current bottlenecks in the network to flow

                if flow < bottleneck:   # checks if that capacity is less than the bottleneck (can fit through the pipe)
                    bottleneck = flow   # sets the new bottleneck if it fits
        return bottleneck

    def remove_flow_capacity(self):
        '''remove flow from network and return both the path and the amount removed'''

        bottleneck = self.return_bottleneck_flow()
        flows = ""
        if bottleneck > 0:
            print "Current Path: " + str(self.route)

        for index, node in enumerate(self.route):   # enumerates through the shortest path in the network
            if index + 1 != len(self.route):    # checks if the position is at the end of the path
                cur_node_path = (ord(self.route[index]) - 65)  # assigns the current node in the path to a variable
                next_node_path = (ord(self.route[index + 1]) - 65)  # assigns the next node in the path to a variable
                flows += str(self.route[index]) + " --> " + str(self.route[index + 1]) + " Original Flow: (" + str(
                    self.network[cur_node_path][next_node_path]) + "), New Flow: ("    # used to print the current flow
                self.network[cur_node_path][next_node_path] -= bottleneck   # takes the bottleneck off of the networks available capacity for the node
                self.network[next_node_path][cur_node_path] += bottleneck   # puts the bottleneck onto the opposite direction in the network to allow reverse flow
                flows += str(self.network[cur_node_path][next_node_path]) + ") \n"
        print "Path Bottleneck: " + str(bottleneck)
        print flows
        return self.route, bottleneck

    def return_max_flow(self):
        '''<--- this method is used to determine what the max flow is of the network
        by running the various methods needed to calculate it, this will then print
        the max flow of the entire network --->'''
        distance = infinity # initially set to infinity for comparison
        maxflow = 0 # initially set to 0 because there is no current max flow

        while distance != 0:    # runs while there is a path in the network to visit
            route, distance = Dijkstra.return_shortest_path(self) # finds the current shortest path
            path, bottleneck = self.remove_flow_capacity()  # finds the bottleneck of that path and removes it from the path (while adding the reverse flow ath too
            maxflow += bottleneck   # adds the current flow to the max flow, to determine an overall "max flow"

            print "Currnet Maxflow:", maxflow

            for index in range(0, len(self.nodetable)): # this will then cycle through the node table and reset all of the nodes to its initial states
                self.nodetable[index].visited = False
                self.nodetable[index].distfromsource = infinity
                self.nodetable[index].previous = invalid_node
            self.nodetable[self.startnode].distfromsource = 0   # including the start node
            self.nodetable[self.startnode].visited = True
            self.route = [] # and clearing the current path

        print "MAX FLOW:", maxflow
        return maxflow

if __name__ == '__main__':
    m = MaxFlow()
    m.populate_network("network8.txt")   # populates the network with the provided "network.txt" file
    m.parse_route("route.txt")  # sets the start and end node to the specified values
    m.return_max_flow() # calculates max flow

    ''' When populating the network you will need to use a text file named "network.txt" this 
    will be populated with comma seperated values for each node in the network, a "route.txt" 
    will also be needed to allow for the start and end nodes to be initially set '''

