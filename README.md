# car_knowledge_graph
基于neo4j的汽车知识图谱，使用flask构建系统，Echarts可视化

本项目源于这门课程： https://study.163.com/course/introduction.htm?courseId=1006292001&_trace_c_p_k2_=9d9fe21f18364c63badf2d3df0523c56

但是原课程的代码中使用的包很多都过时了，所以我用flask重构了原本的django代码，neo4j也换成了4.x

### 安装

直接 pip install -r requirements.txt 即可

neo4j使用的是 neo4j-community-4.0.1 

### 导入数据

数据和使用说明都在data目录下

导入时要将数据放在neo4j的import目录下，不然会提示找不到数据

### 实体查询

![Alt text](https://github.com/luxuantao/car_knowledge_graph/blob/master/img/entity.png)

### 关系查询

![Alt text](https://github.com/luxuantao/car_knowledge_graph/blob/master/img/relation.png)

### 未来

其实项目中可以改进的点很多，读者也可以此项目为模板，开发更多不同类型的知识图谱