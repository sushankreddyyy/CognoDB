from app import create_app


def test_home_page():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'GraphPath' in response.data


def test_recommendations():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        response = client.get('/api/recommendations')
        assert response.status_code == 200
        payload = response.get_json()
        assert payload['recommendations']
