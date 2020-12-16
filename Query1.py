import csv

import pymongo


class Q1:
    __instance = None

    @staticmethod
    def get_instance():
        if Q1.__instance is None:
            Q1()
        print('Connection with PyMongo DB established !!')
        return Q1.__instance

    def __init__(self):
        if Q1.__instance is not None:
            raise Exception('This class is a singleton!')

        Q1.__instance = self
        self.my_client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.my_db = self.my_client['HeitoNet']
        self.my_diseases = self.my_db['Diseases']
        self.my_names = self.my_db['Names']
        self.mapper = {}
        self.my_client.server_info()

    def delete_data(self):
        self.my_db.drop_collection('Names')
        self.my_db.drop_collection('Diseases')
        print('MongoDB Deleted')

    def load_nodes(self, file_name: str):
        tsv_file = open(file_name)
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        next(read_tsv)
        for row in read_tsv:
            self.add_node(row[0], row[1], row[2])
        tsv_file.close()
        print('MongoDB nodes has been read')

    def add_node(self, node_id: str, node_name: str, node_kind: str):
        if node_kind.__eq__('Disease'):
            self.my_diseases.insert_one({"_id": node_id, "name": node_name, "Drugs": [], "Genes": [], "Anatomy": []})
        else:
            self.my_names.insert_one({"_id": node_id, "name": node_name})
            self.mapper[node_id] = node_name

    def load_edges(self, file_name: str):
        tsv_file = open(file_name)
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        next(read_tsv)
        for row in read_tsv:
            self.add_edge(row[0], row[1], row[2])
        tsv_file.close()
        print('MongoDB edges has been read')

    def _get_name(self, node_id: str) -> str:
        if node_id in self.mapper:
            return self.mapper[node_id]

        node = self.my_names.find_one({"_id": node_id})
        return node['name'] if node else None

    def add_edge(self, source_id: str, relation: str, destination_id: str):
        if (relation[0] == 'D' and relation[2] == 'D') or (relation[0] != 'D' and relation[2] != 'D'):
            return
        if relation[2] == 'D':  # CtD CpD
            drug_name = self._get_name(source_id)
            if drug_name:
                self.my_diseases.update_one({"_id": destination_id}, {"$push": {"Drugs": drug_name}})
        elif relation[2] == 'A':  # DlA
            anatomy_name = self._get_name(destination_id)
            if anatomy_name:
                self.my_diseases.update_one({"_id": source_id}, {"$push": {"Anatomy": anatomy_name}})
        else:  # DdG DaG DuG
            gene_name = self._get_name(destination_id)
            if gene_name:
                self.my_diseases.update_one({"_id": source_id}, {"$push": {"Genes": gene_name}})

    def printer(self):
        print('MongoDB Names')
        for i in self.my_names.find():
            print(i)

        print('MongoDB Diseases')
        for i in self.my_diseases.find():
            print(i)

    def query(self, disease_id: str):
        print(self.my_diseases.find_one({"_id": disease_id}))
