# Location to store files /var/lib/neo4j/import/
# sudo service neo4j start
# sudo systemctl start mongod
# add1 Input/sample_nodes.tsv Input/sample_edges.tsv
# add1 test/nodes_test.tsv test/edges_test.tsv


from Query1 import Q1
from Query2 import Q2


def app():
    q1, q2 = establish_connection()
    while True:
        query = input(">>> ").split()
        if len(query) < 1:
            continue
        keyword = query[0].lower()
        if keyword.__eq__('add1'):
            load_data(query[1:], q1)
        elif keyword.__eq__('add2'):
            load_data(query[1:], q2)
        elif keyword.__eq__('delete1'):
            q1.delete_data()
        elif keyword.__eq__('delete2'):
            q2.delete_data()
        elif keyword.__eq__('q1'):
            q1.query(' '.join(query[1:]))
        elif keyword.__eq__('q2'):
            q2.query(' '.join(query[1:]))
        elif keyword.__eq__('printer1'):
            q1.printer()
        elif keyword.__eq__('printer2'):
            q2.printer()
        elif keyword.__eq__('exit'):
            print('Good Bye, I hope you enjoyed using my App !!!')
            break
        else:
            print('Unexpected Input')


def establish_connection() -> (Q1, Q2):
    try:
        return Q1.get_instance(), Q2.get_instance()
    except:
        print('Connection with one or both of the databases Can\'t be established')
        exit()


def load_data(files_names: [], q):
    if len(files_names) != 2:
        print('Input Format is wrong')
        print('Format should be: Add NodesFileName EdgesFileName')
        return

    q.load_nodes(files_names[0])
    q.load_edges(files_names[1])


if __name__ == '__main__':
    app()

# COVID-19 Disease::XLID:00001
