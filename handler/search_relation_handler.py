from toolkit.pre_load import neo4jconn
import os
import json


relationCountDict = {}
filePath = os.path.abspath(os.path.join(os.getcwd(),"."))

with open(filePath+"/toolkit/relationStaticResult.txt","r") as fr:
	for line in fr:
		relationNameCount = line.split(",")
		relationName = relationNameCount[0][2:-1]
		relationCount = relationNameCount[1][1:-2]
		relationCountDict[relationName] = int(relationCount)

def sortDict(relationDict):
	for i in range(len(relationDict)):
		relationName = relationDict[i]['rel']['type']
		relationCount = relationCountDict.get(relationName)
		if relationCount is None:
			relationCount = 0
		relationDict[i]['relationCount'] = relationCount
	relationDict = sorted(relationDict,key = lambda item:item['relationCount'],reverse = True)
	return relationDict

def search_relation(entity1, relation, entity2):
	db = neo4jconn
	entity1 = entity1.strip()
	entity2 = entity2.strip()
	relation_map = {1: '无限制'}
	#若只输入entity1,则输出与entity1有直接关系的实体和关系
	if len(entity1) != 0 and relation == 1 and len(entity2) == 0:
		searchResult = db.findRelationByEntity1(entity1)
		searchResult = sortDict(searchResult)
		if len(searchResult) > 0:
			return {'ctx': '', 'searchResult':json.dumps(searchResult, ensure_ascii=False)}

	#若只输入entity2则,则输出与entity2有直接关系的实体和关系
	if len(entity2) != 0 and relation == 1 and len(entity1) == 0:
		searchResult = db.findRelationByEntity2(entity2)
		searchResult = sortDict(searchResult)
		if len(searchResult) > 0:
			return {'ctx': '', 'searchResult':json.dumps(searchResult, ensure_ascii=False)}

	#若输入entity1和relation，则输出与entity1具有relation关系的其他实体
	if len(entity1) != 0 and relation != 1 and len(entity2) == 0:
		relation = relation_map[relation]
		searchResult = db.findOtherEntities(entity1, relation)
		searchResult = sortDict(searchResult)
		if len(searchResult) > 0:
			return {'ctx': '', 'searchResult':json.dumps(searchResult, ensure_ascii=False)}

	#若输入entity2和relation，则输出与entity2具有relation关系的其他实体
	if len(entity2) != 0 and relation != 1 and len(entity1) == 0:
		relation = relation_map[relation]
		searchResult = db.findOtherEntities2(entity2, relation)
		searchResult = sortDict(searchResult)
		if len(searchResult) > 0:
			return {'ctx': '', 'searchResult':json.dumps(searchResult, ensure_ascii=False)}

	#若输入entity1和entity2,则输出entity1和entity2之间的关系
	if len(entity1) != 0 and relation == 1 and len(entity2) != 0:
		searchResult = db.findRelationByEntities(entity1, entity2)
		print(searchResult)
		searchResult = sortDict(searchResult)
		if len(searchResult) > 0:
			return {'ctx': '', 'searchResult':json.dumps(searchResult, ensure_ascii=False)}

	#若输入entity1,entity2和relation,则输出entity1、entity2是否具有相应的关系
	if len(entity1) != 0 and len(entity2) != 0 and relation != 1:
		relation = relation_map[relation]
		searchResult = db.findEntityRelation(entity1, relation, entity2)
		searchResult = sortDict(searchResult)
		if len(searchResult) > 0:
			return {'ctx': '', 'searchResult':json.dumps(searchResult, ensure_ascii=False)}

	return {'ctx': 'padding', 'searchResult': ''}
