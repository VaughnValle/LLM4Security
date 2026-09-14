from schemas import AgentRole, Finding, Task
def test_task_schema():
    t=Task(task_id='t1',agent=AgentRole.ANALYST,objective='Inspect auth logic'); assert t.task_id=='t1'
def test_finding_confidence_bounds():
    f=Finding(finding_id='f1',title='Candidate issue',description='Example',confidence=0.5); assert f.confidence==0.5
