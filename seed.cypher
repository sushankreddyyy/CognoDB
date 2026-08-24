// GraphPath seed data. Run through scripts/seed.py, which uses the official Neo4j driver.

CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT role_id IF NOT EXISTS FOR (r:Role) REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT company_name IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE;

UNWIND [
  {id:'person_sushank', name:'Sushank', skills:['Python','SQL','Machine Learning','Deep Learning']},
  {id:'person_ananya', name:'Ananya', skills:['Python','SQL','Data Analysis']},
  {id:'person_rohan', name:'Rohan', skills:['Java','SQL','Cloud']}
] AS pData
MERGE (p:Person {id:pData.id}) SET p.name=pData.name
WITH p, pData
UNWIND pData.skills AS skillName
MERGE (s:Skill {name:skillName})
MERGE (p)-[:HAS_SKILL]->(s);

UNWIND [
  {id:'ml_engineer', title:'Machine Learning Engineer', type:'Product / AI', description:'Build, evaluate and deploy ML models.', skills:['Python','Machine Learning','SQL','Deep Learning']},
  {id:'data_scientist', title:'Data Scientist', type:'Analytics', description:'Turn data into experiments, insights and predictive models.', skills:['Python','SQL','Machine Learning']},
  {id:'backend_python', title:'Python Backend Engineer', type:'Software', description:'Design APIs and data-backed services with Python.', skills:['Python','SQL','Cloud']},
  {id:'ai_engineer', title:'AI Engineer', type:'AI Platform', description:'Build applied AI features using deep learning and machine learning.', skills:['Python','Deep Learning','Machine Learning']},
  {id:'data_engineer', title:'Data Engineer', type:'Data Platform', description:'Build reliable pipelines and analytical data systems.', skills:['Python','SQL','Cloud']},
  {id:'cloud_engineer', title:'Cloud Engineer', type:'Infrastructure', description:'Build and operate scalable cloud infrastructure.', skills:['Cloud','Python','SQL']}
] AS rData
MERGE (r:Role {id:rData.id})
SET r.title=rData.title, r.company_type=rData.type, r.description=rData.description
WITH r, rData
UNWIND rData.skills AS skillName
MERGE (s:Skill {name:skillName})
MERGE (r)-[:REQUIRES]->(s);

UNWIND [
  {name:'Nova AI Labs', roles:['ml_engineer','ai_engineer']},
  {name:'Signal Analytics', roles:['data_scientist']},
  {name:'CraftCloud', roles:['backend_python','cloud_engineer']},
  {name:'GraphWorks', roles:['ml_engineer','data_engineer']},
  {name:'DataOrbit', roles:['data_engineer','data_scientist']}
] AS cData
MERGE (c:Company {name:cData.name})
WITH c,cData
UNWIND cData.roles AS roleId
MATCH (r:Role {id:roleId})
MERGE (c)-[:OFFERS]->(r);
