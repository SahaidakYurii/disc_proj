"""
Module that checks connectivity of graphs.
"""

import copy

########################
#        Task 1
########################
def read_graph(path: str, directed = True) -> dict[int, list[int]]:
    """
    Reads graph represented as matrix in .csv file and returns it as a dictionary

    If the graph is directed all vertexes added to the dictionary in two directions from vert_1 to
    vert_2 and from vert_2 to vert_1
    """
    # Initialises empty dictionary for graph
    graph = {}

    with open(path, "r", encoding='utf-8') as file:
        # According to the task, each line containe info about one edge
        for line in file:
            content = line.strip().split(",")
            vert_1 = int(content[0])
            vert_2 = int(content[1])

            # If vertex is not initialised in graph, function adds it
            if vert_1 not in graph:
                graph[vert_1]=[]

            graph[vert_1].append(vert_2)

            # Initialises vertex with no connections if it is mentioned in any of the edges
            if vert_2 not in graph:
                graph[vert_2] = []

            # If the graph is not directed, the function also adds edge from vert_2 to vert_1
            if not directed:
                graph[vert_2].append(vert_1)

    return graph

########################
#        Task 2
########################
def write_graph(path: str, graph: dict[int, list[int]], directed = True) -> None:
    """
    Writes the graph to a csv file with the path. If directed is False, edges represented as
    vert_1 - vert_2 and vert_2 - vert_2 considered to be the same and written to the file only once
    """
    with open(path, "w", encoding="utf-8") as file:
        # Initialises empty string for cotest of the file
        text = ""

        # Iterates through all of the vertexes
        for vert_1 in graph:
            for vert_2 in graph[vert_1]:
                line = str(vert_1) + "," + str(vert_2) + "\n"
                inverted_line = str(vert_2) + ',' + str(vert_2)

                # If graph is directed, dunction simply adds every edge
                #
                # If graph is not directed, the function does not edd edge
                # to file if it sinverted copy is in text
                if directed or (not directed and inverted_line not in text):
                    text += line

        file.write(text.strip())

########################
#        Task 3
########################
def bfs(graph: dict[int, list[int]], start:int) -> list[int]:
    """
    Commits breadth-first search for graph beginings with vertex. Returns list of vertexes sorted
    by number of nodes needed to be passed to enter the vertex

    >>> graph = {0: [1], 1: [3], 2: [0, 3], 3:[2]}
    >>> bfs(graph, 0)
    [0, 1, 3, 2]

    >>> graph = {0: [2], 1: [3], 2: [1, 3], 3:[1, 4], 4:[]}
    >>> bfs(graph, 0)
    [0, 2, 1, 3, 4]

    >>> graph = {0: [2], 1: [3, 4], 2: [1, 3], 3:[1, 4], 4:[]}
    >>> bfs(graph, 0)
    [0, 2, 1, 3, 4]
    """
    # Initialises lists that starts with start vertex
    list_bfs = [start]
    next_key = [start]

    while next_key:
        # Key is the vertex that is checked
        key = next_key.pop(0)

        # Iterates through all related vertexes and adds them to the lists
        for rel_vert in graph[key]:
            if rel_vert not in list_bfs:
                list_bfs.append(rel_vert)
                next_key.append(rel_vert)

    return list_bfs

def find_connected_components(graph: dict[int, list[int]]) -> list[int]:
    """
    Splits graph to connected components. Returns list of components represented by the smallest
    vertexes of the component

    >>> graph = {0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3, 5], 5: [4], 6: [7], 7: [6]}
    >>> find_connected_components(graph)
    [0, 3, 6]

    >>> graph = {0: []}
    >>> find_connected_components(graph)
    [0]

    >>> graph = {}
    >>> find_connected_components(graph)
    []
    """
    # Initialises empty list of connectivity components
    comps = []

    # Iterates through all vertexes of the graph and adds result of bfs to component list as it is
    # a list of vertexes in one connected component
    for vert in graph:
        rel_verts = bfs(graph, vert)

        if set(rel_verts) not in comps:
            comps += [set(rel_verts)]

    # Returns a list of vertexes with minimum numbers as they represents a connectivity component
    return [min(i) for i in comps]

########################
#        Task 4
########################
def find_cycle(graph: dict[int: list[int]], vertex: int) -> tuple[list[int], bool]:
    """
    Dict, Int -> List, Bool

    Commits depth-first search for graph beginings with vertex. Returns list of vertexes sorted
    by number of nodes needed to be passed to enter the vertex. Returns empty list if there is no
    cycle which begins with the vertex.

    >>> graph = {0: [1], 1: [2], 2: [0, 1], 3: [2], 4: [5, 3], 5: [4]}
    >>> vertex = 4
    >>> find_cycle(graph, vertex)
    ([4, 5], True)

    >>> graph = {0: [1, 2], 1: [3], 2: [0], 3: [4], 4: [0]}
    >>> vertex = 0
    >>> find_cycle(graph, vertex)
    ([0, 1, 3, 4], True)

    >>> graph = {0: [1], 1: [2], 2: [0, 1], 3: [4], 4: [5], 5: [4]}
    >>> vertex = 3
    >>> find_cycle(graph, vertex)
    ([], False)

    >>> graph = {0: [1, 2], 1: [3], 2: [0], 3: [4], 4: [0]}
    >>> vertex = 0
    >>> find_cycle(graph, vertex)
    ([0, 1, 3, 4], True)
    """
    # Initialises path as empty list and copies stack. Sorts it by descending
    path = [vertex]
    visited = []
    stack = copy.copy(graph[vertex])
    stack.sort(reverse=True)

    # while stack is not empty
    while stack:
        # Takes last vertex as new one
        sub_vert = stack[-1]
        stack = stack[:-1]
        path.append(sub_vert)
        visited.append(sub_vert)

        # Loks at related vertexes
        rels = [vert for vert in copy.copy(graph[sub_vert]) if vert not in visited + stack]
        rels.sort(reverse=True)

        # If vertex is in related, the cycle is found
        if vertex in rels:
            return (path, True)

        # If rels is empty, returns to previous vertex and goes to another related vertex and
        # removes curent vertex from path
        if rels == []:
            # returns to the nearest vertex that has a relative vertex
            temp_rels = [vert for vert in copy.copy(graph[path[-1]]) if vert not in visited]
            while not temp_rels:
                # Checks if path[-1] exists. If not, it means that there is no cycle
                if len(path) == 1:
                    return ([], False)

                path = path[:-1]
                temp_rels = [vert for vert in copy.copy(graph[path[-1]]) if vert not in visited]
        # If not removes vertex from stack and adds its rels in it
        else:
            stack = stack + rels

    # If cycle was not found, returns False
    return ([], False)


def find_strongly_connected_components(graph: dict[int: list[int]]) -> list[int]:
    """
    Splits graph to strongly connected components. Returns list of components represented by the
    smallest vertexes of the component

    >>> graph = {0: [1], 1: [2], 2: []}
    >>> find_strongly_connected_components(graph)
    []

    >>> graph = {0: [1], 1: [2], 2: [0, 1], 3: [4], 4: [5], 5: [4]}
    >>> find_strongly_connected_components(graph)
    [0, 4]

    >>> graph = {0: [1, 2], 1: [3], 2: [0], 3: [4], 4: [0]}
    >>> find_strongly_connected_components(graph)
    [0]
    """

    # Initialises empty list for connected components amd a list of all vertexes of the fraph
    comps = []
    vertexes = list(graph.keys())

    # Iterates through all vertexes of the graph and calls find_cycle for every. Result of
    # find_cycle is a strongly connected component
    while vertexes:
        vertex = vertexes[0]
        rels, iscycle = find_cycle(graph, vertex)

        # For all related vertexes result of find_cycle is the same but in different order. So the
        # function deletes all strongly connected vertexes from list
        if iscycle:
            # Remover vertexes of the cycle
            for vert in rels:
                if vert in vertexes:
                    vertexes.remove(vert)

            # Finds a vertex with the smallest index and adds it to components list
            index = min(rels)
            if index not in comps:
                comps.append(min(rels))
        else:
            vertexes.remove(vertex)

    return comps

########################
#        Task 5
########################
def find_connectivity_spots(graph: dict[int, list[int]]) -> list[int]:
    """
    Finds connectivity spots of the graph

    >>> graph = {0: [1, 3, 4], 1: [0, 2], 2: [1, 3], 3: [0, 2], 4: [0]}
    >>> find_connectivity_spots(graph)
    [0]

    >>> graph = {0: [1, 3, 4], 1: [0, 2], 2: [1, 3], 3: [0, 2], 4: [0, 5], 5: [4, 6], 6: [5]}
    >>> find_connectivity_spots(graph)
    [0, 4, 5]

    >>> graph = {0: [], 1: [], 2: [3], 3: [2]}
    >>> find_connectivity_spots(graph)
    []
    """
    graphs_comps = find_connected_components(graph)
    # New graph without a vertex
    temp_graph = {}

    rel_vertexes = []
    result = []

    for del_vert in graph:
        temp_graph={}

        # Iterates through dictionary and creates copy of graph which does not contain any
        # connection with del_vert
        for vertex in graph:
            for sub_vert in graph[vertex]:
                # Adds edge to temp_graph only if it is not related to del_vert
                if del_vert != sub_vert:
                    rel_vertexes.append(sub_vert)

            if vertex != del_vert:
                temp_graph[vertex] = rel_vertexes

            rel_vertexes = []

        # If number of connectivity components of graph and temp_graph differs
        if len(graphs_comps) < len(find_connected_components(temp_graph)):
            result.append(del_vert)

        temp_graph = {}

    return result

########################
#        Task 6
########################
def del_edge(graph: dict[int, list[int]], edge: tuple[int, int]) -> dict[int, list[int]]:
    """
    Deletes an edge from the graph and return a new graph.

    >>> del_edge({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (2, 4))
    {1: [2, 5], 2: [1], 3: [4], 4: [3], 5: [1]}
    """
    if edge[1] in graph[edge[0]]:
        graph[edge[0]].remove(edge[1])

    if edge[0] in graph[edge[1]]:
        graph[edge[1]].remove(edge[0])

    return graph


def find_bridges(graph: dict[int, list[int]]) -> list[tuple[int]]:
    """
    function deletes edge and checks if number of connected components has changed

    >>> graph = {0: [1, 2, 3], 1: [0, 2], 2: [0, 1], 3: [0, 4], 4: [3, 5], 5: [4]}
    >>> find_bridges(graph)
    [(0, 3), (3, 4), (4, 5)]

    >>> graph = {0: [1, 2, 3], 1: [0, 2], 2: [0, 1], 3: [0, 4, 5], 4: [3, 5], 5: [3, 4]}
    >>> find_bridges(graph)
    [(0, 3)]
    """
    # Initialises empty list of bridges
    list_of_bridges = []

    # Iterates through all elements of the graph
    for vertex1 in graph:
        for vertex2 in graph[vertex1]:
            current_edge = (vertex1, vertex2)
            new_graph = copy.deepcopy(graph)
            new_graph = del_edge(new_graph, current_edge)

            # if number of connected components has increased -> current edge is a bridge
            if find_connected_components(graph) < find_connected_components(new_graph):
                if (current_edge[1], current_edge[0]) not in list_of_bridges:
                    list_of_bridges.append(current_edge)

    return list_of_bridges

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
