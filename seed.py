from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("COGNODB_URI")
USER = os.getenv("COGNODB_USER", "cognodb")
PASSWORD = os.getenv("COGNODB_PASSWORD")

if not URI or not PASSWORD:
    raise SystemExit("Set COGNODB_URI and COGNODB_PASSWORD in .env before seeding.")

cypher = Path(__file__).resolve().parents[1].joinpath("data", "seed.cypher").read_text()
statements = [s.strip() for s in cypher.split(";") if s.strip()]

with GraphDatabase.driver(URI, auth=(USER, PASSWORD)) as driver:
    driver.verify_connectivity()
    with driver.session() as session:
        for statement in statements:
            session.run(statement).consume()

print(f"Seed complete: executed {len(statements)} Cypher statements.")
