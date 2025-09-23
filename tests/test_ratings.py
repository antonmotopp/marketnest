from fastapi import status


def test_create_rating_after_purchase_success(client, auth_tokens):
    seller_token, buyer_token = auth_tokens

    form_data = {
        'title': 'Item for Rating',
        'description': 'Will be rated',
        'price': '100.00',
        'category': 'electronics'
    }

    create_response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {seller_token}"},
        data=form_data
    )
    ad_id = create_response.json()["id"]

    client.patch(
        f"/advertisements/{ad_id}/buy",
        headers={"Authorization": f"Bearer {buyer_token}"}
    )

    response = client.post(
        "/ratings/",
        headers={"Authorization": f"Bearer {buyer_token}"},
        json={
            "reviewed_user_id": 1,
            "advertisement_id": ad_id,
            "rating": 4,
            "comment": "Good seller"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["rating"] == 4
    assert data["reviewed_user_id"] == 1


def test_create_rating_without_transaction_fails(client, auth_tokens):
    seller_token, buyer_token = auth_tokens

    response = client.post(
        "/ratings/",
        headers={"Authorization": f"Bearer {buyer_token}"},
        json={
            "reviewed_user_id": 1,
            "advertisement_id": 999,
            "rating": 4,
            "comment": "Cannot rate"
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_ratings_empty_list(client):
    response = client.get("/ratings/999")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []