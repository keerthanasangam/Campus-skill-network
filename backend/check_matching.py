from database.databricks import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
SELECT
    os.opportunity_id,
    s.skill_name,
    os.importance
FROM workspace.default.opportunity_skills os
JOIN workspace.default.skills s
    ON os.skill_id = s.skill_id
ORDER BY os.opportunity_id
LIMIT 30
""")

print("OPPORTUNITY SKILLS:")
print(*cursor.fetchall(), sep="\n")

cursor.close()
connection.close()