from py2neo import Graph, Node, Relationship, NodeMatcher


class Neo4j_Handle():
    graph = None

    # matcher = None
    def __init__(self):
        print("Neo4j Init ...")

    def connectDB(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="12345678")

    # self.matcher = NodeMatcher(self.graph)

    # 实体查询，用于命名实体识别：品牌+车系+车型
    def matchEntityItem(self, value):
        answer = self.graph.run("MATCH (entity1) WHERE entity1.name = \"" + value + "\" RETURN entity1").data()
        return answer

    # 实体查询
    def getEntityRelationbyEntity(self, value):
        # 查询实体：不考虑实体类型，只考虑关系方向
        answer = self.graph.run(
            "MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + value + "\" RETURN rel,entity2").data()
        if (len(answer) == 0):
            # 查询实体：不考虑关系方向
            answer = self.graph.run(
                "MATCH (entity1) - [rel] - (entity2)  WHERE entity1.name = \"" + value + "\" RETURN rel,entity2").data()
        print(answer)
        return answer

    # 关系查询:实体1
    def findRelationByEntity1(self, entity1):
        # 基于品牌查询
        answer = self.graph.run("MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel] -> (n2) RETURN n1,rel,n2").data()
        # 基于车系查询，注意此处额外的空格
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel] - (n2) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体2
    def findRelationByEntity2(self, entity1):
        # 基于品牌
        answer = self.graph.run("MATCH (n1)<- [rel] - (n2:Bank {name:\"" + entity1 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            # 基于车系
            answer = self.graph.run(
                "MATCH (n1) - [rel] - (n2:Series {name:\"" + entity1 + "\"}) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体1+关系
    def findOtherEntities(self, entity, relation):
        answer = self.graph.run(
            "MATCH (n1:Bank {name:\"" + entity + "\"})- [rel:Subtype {type:\"" + relation + "\"}] -> (n2) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：关系+实体2
    def findOtherEntities2(self, entity, relation):
        print("findOtherEntities2==")
        print(entity, relation)
        answer = self.graph.run(
            "MATCH (n1)- [rel:RELATION {type:\"" + relation + "\"}] -> (n2:Bank {name:\"" + entity + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1)- [rel:RELATION {type:\"" + relation + "\"}] -> (n2:Series {name:\"" + entity + "\"}) RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体1+实体2(注意Entity2的空格）
    def findRelationByEntities(self, entity1, entity2):
        # 品牌 + 品牌
        answer = self.graph.run(
            "MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel] -> (n2:Bank{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            # 品牌 + 系列
            print(
                "MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel] -> (n2:Series{name:\"" + entity2 + "\"}) RETURN n1,rel,n2")
            answer = self.graph.run(
                "MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel] -> (n2:Series{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            # 系列 + 品牌
            answer = self.graph.run(
                "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel] -> (n2:Bank{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            # 系列 + 系列
            answer = self.graph.run(
                "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel] -> (n2:Series{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        return answer

    # 查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self, entity1, relation, entity2):
        answer = self.graph.run(
            "MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel:subbank {type:\"" + relation + "\"}] -> (n2:Bank{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1:Bank {name:\"" + entity1 + "\"})- [rel:subbank {type:\"" + relation + "\"}] -> (n2:Series{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel:subbank {type:\"" + relation + "\"}] -> (n2:Bank{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        if (len(answer) == 0):
            answer = self.graph.run(
                "MATCH (n1:Series {name:\"" + entity1 + "\"})- [rel:subbank {type:\"" + relation + "\"}] -> (n2:Series{name:\"" + entity2 + "\"}) RETURN n1,rel,n2").data()
        return answer
