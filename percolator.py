class PercolationPlayer:
    class ModifiedGraph:
        def __init__(self, graph):
            vertices = {v: set() for v in graph.V}
            for e in graph.E:
                vertices[e.a].add(e.b)
                vertices[e.b].add(e.a)
            self.adj_list = {k:set(v) for k,v in vertices.items()}
            
        def GetVertices(self, player):
            my_vertices = {}
            opp_vertices = {}
            free_vertices = {}
            for v, vertices in self.adj_list.items():
                if v.color == player:
                    my_vertices[v] = vertices
                if v.color == -1:
                    free_vertices[v] = vertices
                else:
                    opp_vertices[v] = vertices
            return my_vertices, opp_vertices, free_vertices

    # `graph` is an instance of a Graph, `player` is an integer (0 or 1).
    # Should return a vertex `v` from graph.V where v.color == -1
    # @profile
    def ChooseVertexToColor(graph, player):
        modified_graph = PercolationPlayer.ModifiedGraph(graph)
        best_v = None
        max_degree = 0
        my_vertices, opp_vertices, free_vertices = modified_graph.GetVertices(player)

        for v, vertices in free_vertices.items():
            if len(vertices) >= max_degree and len(vertices.intersection(my_vertices)) != 0:
                best_v = v
                max_degree = len(vertices)
        
        if best_v == None:
            for v, vertices in free_vertices.items():
                if len(vertices) >= max_degree:
                    best_v = v
                    max_degree = len(vertices)

        return best_v

    # `graph` is an instance of a Graph, `player` is an integer (0 or 1).
    # Should return a vertex `v` from graph.V where v.color == player
    # @profile
    def ChooseVertexToRemove(graph, player):
        modified_graph = PercolationPlayer.ModifiedGraph(graph)
        my_vertices, opp_vertices, free_vertices = modified_graph.GetVertices(player)

        v_scores = {}

        for v, vertices in my_vertices.items():
            score = 0
            for v2 in vertices:
                if v2.color == player:
                    score -= 1
                else:
                    score += 1
            v_scores[abs(score)] = v

        min_score = min(v_scores.keys(), key = abs)
        return v_scores[min_score]