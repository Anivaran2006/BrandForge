from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'ok'


def test_projects_endpoint_lists_created_projects():
    create_resp = client.post('/api/projects', json={'idea': 'A focused productivity studio.'})
    assert create_resp.status_code == 201

    response = client.get('/api/projects')
    assert response.status_code == 200
    assert any(project['project_id'] == create_resp.json()['project_id'] for project in response.json()['projects'])


def test_project_details_can_be_updated():
    create_resp = client.post('/api/projects', json={'idea': 'A focused productivity studio.'})
    project_id = create_resp.json()['project_id']

    response = client.put(
        f'/api/projects/{project_id}',
        json={'audience': 'independent creators', 'problem': 'Creative work is hard to prioritize.'},
    )

    assert response.status_code == 200
    assert response.json()['audience'] == 'independent creators'
    assert response.json()['problem'] == 'Creative work is hard to prioritize.'


def test_full_workflow_demo():
    create_resp = client.post('/api/projects', json={
        'idea': 'A platform that helps college students find the right teammates for hackathons.',
        'audience': 'college students',
        'industry': 'education',
        'problem': 'Students struggle to find complementary skills and trustworthy teammates before deadlines.'
    })
    assert create_resp.status_code == 201, create_resp.text
    project = create_resp.json()
    project_id = project['project_id']

    for stage in ['discover', 'position', 'define', 'express', 'challenge', 'finalize', 'launch']:
        resp = client.post(f'/api/projects/{project_id}/{stage}')
        assert resp.status_code == 200, resp.text
        payload = resp.json()
        assert payload['project_id'] == project_id
        assert payload['stage'] == stage
        if stage == 'launch':
            assert payload['workflow_stage'] == 'complete'

    export_resp = client.get(f'/api/projects/{project_id}/export')
    assert export_resp.status_code == 200, export_resp.text
    exported = export_resp.json()
    assert exported['final_brand_system']['brand_name']
    assert exported['final_brand_system']['tagline']
    assert exported['markdown_export']
    assert 'Launch Plan' in exported['markdown_export']
