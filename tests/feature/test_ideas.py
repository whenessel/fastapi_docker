import json

from faker import Faker
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.models import Idea


def test_get_ideas(session: Session, client: TestClient):
    response = client.get("/ideas", headers={"tenant": "fake_tenant_company_for_test_00000000000000000000000000000000"})
    response.json()
    assert response.status_code == 200


def test_add_ideas(session: Session, client: TestClient):

    fake = Faker()

    data = {
        "title": fake.text(max_nb_chars=20),
        "description": fake.paragraph(nb_sentences=1),
        "color": fake.safe_color_name(),
        "body_html": "<h1>asd</h1><p>asasd</p>",
        "body_json": {
            "type": "doc",
            "content": [
                {"type": "heading", "attrs": {"level": 1}, "content": [{"type": "text", "text": "asd"}]},
                {"type": "paragraph", "content": [{"type": "text", "text": "asasd"}]},
            ],
        },
    }
    headers = {
        "tenant": "fake_tenant_company_for_test_00000000000000000000000000000000",
        "Content-Type": "application/json",
    }
    response = client.post("/ideas/", data=json.dumps(data), headers=headers)
    data = response.json()
    logger.info(data)
    assert response.status_code == 200


def test_get_idea(session: Session, client: TestClient):
    idea = session.execute(select(Idea).order_by(func.random()).limit(1)).scalar_one()
    response = client.get(
        "/ideas/" + str(idea.uuid), headers={"tenant": "fake_tenant_company_for_test_00000000000000000000000000000000"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["color"] == idea.color
    assert data["title"] == idea.title
    assert data["description"] == idea.description
    assert data["uuid"] == str(idea.uuid)


# def test_delete_idea(session: Session, client: TestClient):
#     idea = session.execute(select(Idea).order_by(func.random()).limit(1)).scalar_one()
#     logger.info(idea.uuid)
#     response = client.delete("/ideas/" + str(idea.uuid), headers={"tenant": "a"})
#     data = response.json()
#     logger.info(data)
#     # {'ok': True}
#     assert response.status_code == 200
