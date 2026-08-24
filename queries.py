# All application queries are parameterised; no user input is concatenated into Cypher.

LIST_SKILLS = """
MATCH (s:Skill)
RETURN s.name AS name, s.category AS category
ORDER BY s.category, s.name
"""

LIST_ROLES = """
MATCH (r:Role)
OPTIONAL MATCH (r)-[:REQUIRES]->(s:Skill)
WITH r, collect(s.name) AS skills
RETURN r.id AS id, r.title AS title, r.company_type AS company_type,
       r.description AS description, skills
ORDER BY r.title
"""

ROLE_DETAIL = """
MATCH (r:Role {id: $role_id})
OPTIONAL MATCH (r)-[:REQUIRES]->(s:Skill)
OPTIONAL MATCH (r)<-[:OFFERS]-(c:Company)
RETURN r.id AS id, r.title AS title, r.company_type AS company_type,
       r.description AS description, collect(DISTINCT s.name) AS skills,
       collect(DISTINCT c.name) AS companies
"""

# 2+ hop traversal: a learner -> skill -> role path.
MATCH_ROLES_BY_SKILLS = """
MATCH (p:Person {id: $person_id})-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES]-(r:Role)
WITH r, count(DISTINCT s) AS matched_skills
OPTIONAL MATCH (r)-[:REQUIRES]->(allSkills:Skill)
WITH r, matched_skills, count(allSkills) AS total_skills
RETURN r.id AS id, r.title AS title, matched_skills, total_skills,
       round(100.0 * matched_skills / CASE WHEN total_skills = 0 THEN 1 ELSE total_skills END, 1) AS fit
ORDER BY fit DESC, matched_skills DESC, r.title
LIMIT 10
"""

# A graph-native query that is awkward in a relational schema:
# recommend a role by traversing Person -> Skill -> Role -> Company in one pattern.
DISCOVER_CAREER_PATHS = """
MATCH pth=(p:Person {id: $person_id})-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES]-(r:Role)<-[:OFFERS]-(c:Company)
WHERE r.id <> $current_role_id
RETURN DISTINCT r.title AS role, c.name AS company,
       [node IN nodes(pth) | labels(node)[0] + ':' + coalesce(node.name, node.title, node.id)] AS path
ORDER BY role, company
LIMIT 20
"""

SEARCH_ROLES = """
MATCH (r:Role)
WHERE toLower(r.title) CONTAINS toLower($q)
   OR toLower(r.description) CONTAINS toLower($q)
RETURN r.id AS id, r.title AS title, r.company_type AS company_type,
       r.description AS description
ORDER BY r.title
LIMIT 20
"""
