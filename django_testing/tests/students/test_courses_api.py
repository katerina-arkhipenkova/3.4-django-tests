import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs, make_m2m=True)

    return factory


@pytest.mark.django_db
def test_get_one_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.get('/api/v1/courses/')
    id = response.data[0]['id']
    name = response.data[0]['name']
    response = client.get(f'/api/v1/courses/{id}/')
    assert response.status_code == 200
    assert response.data['name'] == name


@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 10


@pytest.mark.django_db
def test_filter_course_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    id = response.data[5]['id']
    response = client.get(f'/api/v1/courses/?id={id}')
    assert response.status_code == 200
    assert response.data[0]['id'] == id


@pytest.mark.django_db
def test_filter_course_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    name = response.data[5]['name']
    response = client.get(f'/api/v1/courses/?name={name}')
    assert response.status_code == 200
    assert response.data[0]['name'] == name


@pytest.mark.django_db
def test_create_course(client):
    course = {'id': 1, 'name': 'test'}
    response = client.post('/api/v1/courses/', data=course)
    assert response.status_code == 201
    assert response.data['name'] == 'test'


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    updated_course = {'name': 'test'}
    response = client.get('/api/v1/courses/')
    id = response.data[4]['id']
    response = client.patch(f'/api/v1/courses/{id}/', data=updated_course)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    assert response.data[4]['name'] == 'test'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 10
    id = response.data[4]['id']
    response = client.delete(f'/api/v1/courses/{id}/')
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 9
