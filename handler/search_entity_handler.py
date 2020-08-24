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
	for i in range( len(relationDict) ):
		relationName = relationDict[i]['rel']['type']
		relationCount = relationCountDict.get(relationName)
		if(relationCount is None ):
			relationCount = 0
		relationDict[i]['relationCount'] = relationCount

	relationDict = sorted(relationDict,key = lambda item:item['relationCount'],reverse = True)
	return relationDict

#实体查询
def search_entity(entity):
	#根据传入的实体名称搜索出关系
	#连接数据库
	db = neo4jconn
	entityRelation = db.getEntityRelationbyEntity(entity)
	if len(entityRelation) == 0:
		#若数据库中无法找到该实体，则返回数据库中无该实体
		return {'ctx': '', 'entityRelation': ''}
	else:
		#返回查询结果
		#将查询结果按照"关系出现次数"的统计结果进行排序
		entityRelation = sortDict(entityRelation)
		return {'ctx': json.dumps(entity, ensure_ascii=False), 'entityRelation': json.dumps(entityRelation, ensure_ascii=False)}
