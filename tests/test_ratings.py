from fastapi import status
import pytest


def test_create_rating_success(client, auth_token):
    response = client.post("/ratings/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "reviewed_user_id": 3,
                               "advertisement_id": 1,
                               "rating": 4,
                               "comment": "satisfaying"
                           }
                           )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data["advertisement_id"] == 1
    assert data["rating"] == 4
    assert data["reviewer_id"] == 1
    assert data["comment"] == "satisfaying"
    assert "id" in data
    assert "created_at" in data

def test_create_rating_unauthorized(client):
    response = client.post("/ratings/",
                           json={
                               "reviewed_user_id": 3,
                               "advertisement_id": 1,
                               "rating": 4,
                               "comment": "satisfaying"
                           })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_rating_with_missing_fields(client, auth_token):
    response = client.post("/ratings/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "reviewed_user_id": 3,
                               "advertisement_id": 1,
                           })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_rating_with_invalid_rating(client, auth_token):
    response = client.post("/ratings/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "reviewed_user_id": 3,
                               "advertisement_id": 1,
                               "rating": 7,
                               "comment": "satisfaying"
                           })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_rating_with_long_comment(client, auth_token):
    response = client.post("/ratings/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "reviewed_user_id": 3,
                               "advertisement_id": 1,
                               "rating": 4,
                               "comment": "Feyenoord wint ook vierde duel, doelpunt en rood voor Hadj Moussa tegen Heerenveen"
                                          " Deel dit artikel Feyenoord heeft ook zijn vierde wedstrijd van dit seizoen "
                                          "gewonnen. De ploeg van coach Robin van Persie won door een goal van Anis Hadj "
                                          "Moussa met 1-0 van sc Heerenveen. De matchwinner kreeg na rust rood en ook de"
                                          " bezoekers eindigden het duel met tien man.Hadj Moussa was met recht de Rotterdamse "
                                          "man van de wedstrijd in De Kuip, maar ook scheidsrechter Robin Hensgens eiste een "
                                          "hoofdrol op en Heerenveen-doelman Bernt Klaverboer was de Friese uitblinker."
                           })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_reviewed_user_id_success(client,auth_token):
    create_response = client.post("/ratings/",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "reviewed_user_id": 3,
                               "advertisement_id": 1,
                               "rating": 4,
                               "comment": "satisfaying"
                           }
                           )


    response = client.get("/ratings/3", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0




def test_with_invalid_reviewed_user_id(client, auth_token):
    response = client.get("/ratings/5",
                          headers={"Authorization": f"Bearer {auth_token}"}
                          )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data=response.json()
    assert data["detail"] == "Not Found"

def test_reviewer_user_id_success(client,auth_token):
    create_response = client.post("/ratings",
                           headers={"Authorization": f"Bearer {auth_token}"},
                           json={
                               "reviewed_user_id": 3,
                               "advertisement_id": 1,
                               "rating": 4,
                               "comment": "satisfaying"
                           }
                           )
    created_id = create_response.json()["reviewer_id"]

    response = client.get(f"/ratings/reviewer/{created_id}", headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_with_invalid_reviewer_user_id(client, auth_token):
    response = client.get("/ratings/reviewer/5",
                          headers={"Authorization": f"Bearer {auth_token}"}
                          )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data=response.json()
    assert data["detail"] == "Not Found"

