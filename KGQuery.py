from py2neo import Graph,Node,Relationship,NodeMatcher

# your local neo4j database's username and password
USERNAME="xxx"
PASSWORD="xxx"

class Query():
    def __init__(self):
        self.graph=Graph("http://localhost:7474", username=USERNAME,password=PASSWORD)

    # Check the score of the movie
    def run(self,cql):
        # find_rela  = test_graph.run("match (n:Person{name:'张学友'})-[actedin]-(m:Movie) return m.title")
        result=[]
        find_rela = self.graph.run(cql)
        for i in find_rela:
            result.append(i.items()[0][1])
        return result

# TITLE='英雄'
#
# if __name__ == '__main__':
#     SQL=Query()
#     result=SQL.run("match (m:Movie)-[]->() where m.title=TITLE return m.rating")
#     print(result)
