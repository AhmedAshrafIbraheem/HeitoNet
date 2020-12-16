from py2neo import Graph


class Q2:
    __instance = None

    @staticmethod
    def get_instance():
        if Q2.__instance is None:
            Q2()
        print('Connection with Neo4j DB established !!')
        return Q2.__instance

    def __init__(self):
        if Q2.__instance is not None:
            raise Exception('This class is a singleton!')

        Q2.__instance = self
        self.graph = Graph(password="neo4jj")
        self.graph.run("Match () Return 1 Limit 1")

    def delete_data(self):
        self.graph.delete_all()
        print('Neo4j Deleted')

    def load_nodes(self, file_name: str):
        self._load_node_similar_labels(file_name, 'Compound')
        self._load_node_similar_labels(file_name, 'Gene')
        self._load_node_similar_labels(file_name, 'Disease')
        self._load_node_similar_labels(file_name, 'Anatomy')
        self.graph.run("CREATE INDEX index_disease_name IF NOT EXISTS FOR (n:Disease) ON (n.name)")
        print('Neo4j nodes has been read')

    def _load_node_similar_labels(self, file_name: str, label: str):
        self.graph.run("Create Constraint unique_{} IF NOT EXISTS on (n:{}) Assert n.id Is Unique".format(label, label))
        self.graph.run('''Using Periodic Commit
        Load CSV With Headers From "file:///{}" As line Fieldterminator "\t"
        With line Where line.kind = '{}'
        Create(n:{} {{id: line.id, name: line.name}} )'''.format(file_name, label, label))

    def load_edges(self, file_name: str):
        accepted_edges = {'CrC', 'CuG', 'CdG', 'CtD', 'CpD', 'AdG', 'AuG', 'DlA'}
        label_value = {'C': 'Compound', 'G': 'Gene', 'A': 'Anatomy', 'D': 'Disease'}
        for edge in accepted_edges:
            self._load_edges_similar_labels(file_name, edge, label_value[edge[0]], label_value[edge[-1]])
        print('Neo4j edges has been read')

    def _load_edges_similar_labels(self, file_name: str, label: str, source: str, target: str):
        self.graph.run('''Using Periodic Commit
        Load CSV With Headers From "file:///{}" As line Fieldterminator "\t"
        With line Where line.metaedge = '{}'
        Match(source:{} {{id:line.source}}), (target:{} {{id:line.target}})
        Create((source)-[:{}]->(target))'''.format(file_name, label, source, target, label))

    def printer(self):
        print("Nodes")
        nodes = self.graph.run("Match (n) Return n")
        for node in nodes:
            print(node)

        print("Edges")
        edges = self.graph.run("Match (n)-[r]->(m) Return r")
        for edge in edges:
            print(edge)

    def query(self, disease_name: str):
        unknown_cures = self.graph.run(
            '''Match (d:Disease{{name:'{}'}})-[:DlA]->(a:Anatomy)-[:AuG|:AdG]->(g:Gene)<-[:CdG|:CuG]-(dc:Compound)-[:CrC*0..1]-(c:Compound)
            Where Not (c)-->(d) And ( (a)-[:AdG]->(g)<-[:CuG]-(dc) OR (a)-[:AuG]->(g)<-[:CdG]-(dc))
            Return collect(Distinct c.name)'''.format(disease_name))

        print(unknown_cures)
