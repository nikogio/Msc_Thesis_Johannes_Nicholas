from manim import *
import networkx as nx

class MovingVertices(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4]
        label_dict = {1:'1',
                      2:'1',
                      3:'3',
                      4:'4'}
        edges = [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)]
        g = Graph(vertices, edges, labels=label_dict)
        self.play(Create(g))
        self.wait()
        self.play(g[1].animate.move_to([1, 1, 0]),
                  g[2].animate.move_to([-1, 1, 0]),
                  g[3].animate.move_to([1, -1, 0]),
                  g[4].animate.move_to([-1, -1, 0]))
        self.wait()

class TreeVertices(Scene):
    def construct(self):
        vertices = [1]
        edges = []
        label_dict = {1:'1'}
        g = nx.Graph(vertices, edges,labels=label_dict)
        self.play(Create(g))
        self.wait()
        label_dict[2]='2'
        self.play(g.animate._add_vertex(2,label=True))
        #self.play(g.animate._add_edge(g[1],g[2]))
        self.wait()

class GraphAutoPosition(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        autolayouts = ["spring", "circular", "kamada_kawai",
                       "planar", "random", "shell",
                       "spectral", "spiral"]
        graphs = [Graph(vertices, edges, layout=lt).scale(0.5)
                  for lt in autolayouts]
        r1 = VGroup(*graphs[:3]).arrange()
        r2 = VGroup(*graphs[3:6]).arrange()
        r3 = VGroup(*graphs[6:]).arrange()
        self.add(VGroup(r1, r2, r3).arrange(direction=DOWN))

class LabeledModifiedGraph(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        g = Graph(vertices, edges, layout="circular", layout_scale=3,
                  labels=True, vertex_config={7: {"fill_color": RED}},
                  edge_config={(1, 7): {"stroke_color": RED},
                               (2, 7): {"stroke_color": RED},
                               (4, 7): {"stroke_color": RED}})
        self.add(g)

class GraphAnimation(Scene):
    def construct(self):
        # Create an empty graph
        graph = Graph(vertices=[],edges=[])

        # Add the first vertex
        vertex_a = graph.add_vertices(1)[0]
        self.add(vertex_a)

        # Add the second vertex and edge
        vertex_b = graph.add_vertices(1)[0]
        graph.add_edge(vertex_a, vertex_b)
        self.play(Create(vertex_b), Create(graph.edges[0]))
        self.wait()