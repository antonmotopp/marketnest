from fastapi import status

def test_create_advertisement_success(client, auth_token):
    form_data = {
        'title': 'iPhone 13 for sale',
        'description': 'Excellent condition, all accessories included',
        'price': '15000.50',
        'category': 'electronics'
    }

    response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["title"] == "iPhone 13 for sale"
    assert data["description"] == "Excellent condition, all accessories included"
    assert data["price"] == 15000.50
    assert data["user_id"] == 1
    assert data["category"] == "electronics"
    assert data["photos"] == []
    assert "id" in data
    assert "created_at" in data


def test_create_advertisement_unauthorized(client):
    form_data = {
        'title': 'iPhone 13',
        'description': 'Phone in good condition',
        'price': '15000.50',
        'category': 'electronics'
    }

    response = client.post("/advertisements/", data=form_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_advertisement_missing_fields(client, auth_token):
    form_data = {
        'title': 'iPhone 13'
    }

    response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_advertisements_empty(client):
    response = client.get("/advertisements/all")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_advertisements_with_data(client, auth_token):
    form_data = {
        'title': 'iPhone 13 for sale',
        'description': 'Excellent condition, all accessories included',
        'price': '15000.50',
        'category': 'electronics'
    }

    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )

    response = client.get("/advertisements/all")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "iPhone 13 for sale"


def test_get_advertisement_by_id_success(client, auth_token):
    form_data = {
        'title': 'MacBook Pro for sale',
        'description': 'Latest model with warranty',
        'price': '25000.00',
        'category': 'electronics'
    }

    create_response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )
    created_id = create_response.json()["id"]

    response = client.get(f"/advertisements/{created_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == created_id
    assert data["title"] == "MacBook Pro for sale"
    assert data["description"] == "Latest model with warranty"


def test_get_advertisement_by_id_not_found(client):
    response = client.get("/advertisements/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Advertisement not found"


def test_update_advertisement_success(client, auth_token):
    form_data = {
        'title': 'Old Title',
        'description': 'Old description',
        'price': '1000.00',
        'category': 'electronics'
    }

    create_response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )
    created_id = create_response.json()["id"]

    update_data = {
        'title': 'Updated Title',
        'description': 'Old description',
        'price': '1500.00',
        'category': 'electronics'
    }

    response = client.put(
        f"/advertisements/{created_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=update_data
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["price"] == 1500.00
    assert data["description"] == "Old description"
    assert data["category"] == "electronics"


def test_update_advertisement_unauthorized(client):
    update_data = {
        'title': 'Updated Title',
        'description': 'desc',
        'price': '100.00',
        'category': 'electronics'
    }

    response = client.put("/advertisements/1", data=update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_advertisement_not_found(client, auth_token):
    update_data = {
        'title': 'Updated Title',
        'description': 'desc',
        'price': '100.00',
        'category': 'electronics'
    }

    response = client.put(
        "/advertisements/999",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=update_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Advertisement not found"


def test_delete_advertisement_success(client, auth_token):
    form_data = {
        'title': 'To Delete',
        'description': 'This will be deleted',
        'price': '1000.00',
        'category': 'electronics'
    }

    create_response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )
    created_id = create_response.json()["id"]

    response = client.delete(
        f"/advertisements/{created_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Advertisement deleted successfully"

    get_response = client.get(f"/advertisements/{created_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_advertisement_unauthorized(client):
    response = client.delete("/advertisements/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_advertisement_not_found(client, auth_token):
    response = client.delete(
        "/advertisements/999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Advertisement not found"


def test_create_advertisement_invalid_category(client, auth_token):
    form_data = {
        'title': 'Test',
        'description': 'Test',
        'price': '100.00',
        'category': 'invalid_category'
    }

    response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_filter_advertisements_by_category(client, auth_token):
    form_data1 = {
        'title': 'Phone',
        'description': 'Test',
        'price': '100.00',
        'category': 'electronics'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data1
    )

    form_data2 = {
        'title': 'Chair',
        'description': 'Test',
        'price': '50.00',
        'category': 'furniture'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data2
    )

    response = client.get("/advertisements/all?category=electronics")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "electronics"


def test_update_advertisement_status_patch(client, auth_token):
    form_data = {
        'title': 'Status Test',
        'description': 'Test description',
        'price': '100.00',
        'category': 'electronics'
    }

    create_response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )
    created_id = create_response.json()["id"]

    response = client.patch(
        f"/advertisements/{created_id}/status",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"new_status": "reserved"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "reserved"


def test_filter_advertisements_by_status(client, auth_token):
    form_data1 = {
        'title': 'Available Item',
        'description': 'Test',
        'price': '100.00',
        'category': 'electronics'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data1
    )

    form_data2 = {
        'title': 'Reserved Item',
        'description': 'Test',
        'price': '50.00',
        'category': 'furniture'
    }
    create_response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data2
    )
    reserved_id = create_response.json()["id"]

    client.patch(
        f"/advertisements/{reserved_id}/status",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"new_status": "reserved"}
    )

    response = client.get("/advertisements/all?status=available")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "available"


def test_create_advertisement_default_status(client, auth_token):
    form_data = {
        'title': 'New Item',
        'description': 'Should be available by default',
        'price': '200.00',
        'category': 'other'
    }

    response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "available"


def test_search_advertisements(client, auth_token):
    form_data1 = {
        'title': 'iPhone 14 Pro',
        'description': 'Latest smartphone with great camera',
        'price': '1000.00',
        'category': 'electronics'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data1
    )

    form_data2 = {
        'title': 'Samsung TV',
        'description': 'High quality television',
        'price': '800.00',
        'category': 'electronics'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data2
    )

    response = client.get("/advertisements/all?search=iPhone")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert "iPhone" in data[0]["title"]

    response = client.get("/advertisements/all?search=camera")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert "camera" in data[0]["description"]


def test_create_advertisement_with_photos(client, auth_token):
    form_data = {
        'title': 'iPhone with photos',
        'description': 'Has photos',
        'price': '1000.00',
        'category': 'electronics'
    }

    files = {
        'photos': ('test.jpg', b'fake image data', 'image/jpeg')
    }

    response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data,
        files=files
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["photos"]) == 1
    assert data["photos"][0].startswith("data:image/jpeg;base64,")


def test_sort_advertisements_by_date(client, auth_token):
    import time

    form_data1 = {
        'title': 'First Item',
        'description': 'Created first',
        'price': '100.00',
        'category': 'electronics'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data1
    )

    time.sleep(1)

    form_data2 = {
        'title': 'Second Item',
        'description': 'Created second',
        'price': '200.00',
        'category': 'electronics'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data2
    )

    response = client.get("/advertisements/all?sort_by=newest")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data[0]["title"] == "Second Item"
    assert data[1]["title"] == "First Item"

    response = client.get("/advertisements/all?sort_by=oldest")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data[0]["title"] == "First Item"
    assert data[1]["title"] == "Second Item"


def test_buy_advertisement_success(client, auth_tokens):
    seller_token, buyer_token = auth_tokens

    form_data = {
        'title': 'Item for Sale',
        'description': 'Available item',
        'price': '100.00',
        'category': 'electronics'
    }

    create_response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {seller_token}"},
        data=form_data
    )
    ad_id = create_response.json()["id"]

    response = client.patch(
        f"/advertisements/{ad_id}/buy",
        headers={"Authorization": f"Bearer {buyer_token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "sold"
    assert data["buyer_id"] == 2


def test_buy_own_advertisement_fails(client, auth_token):
    form_data = {
        'title': 'My Item',
        'description': 'Cannot buy own item',
        'price': '100.00',
        'category': 'electronics'
    }

    create_response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )
    ad_id = create_response.json()["id"]

    response = client.patch(
        f"/advertisements/{ad_id}/buy",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cannot buy your own item" in response.json()["detail"].lower()


def test_buy_unavailable_advertisement_fails(client, auth_tokens):
    seller_token, buyer_token = auth_tokens

    form_data = {
        'title': 'Sold Item',
        'description': 'Already sold',
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
        f"/advertisements/{ad_id}/status",
        headers={"Authorization": f"Bearer {seller_token}"},
        json={"new_status": "reserved"}
    )

    response = client.patch(
        f"/advertisements/{ad_id}/buy",
        headers={"Authorization": f"Bearer {buyer_token}"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not available" in response.json()["detail"].lower()


def test_buy_advertisement_unauthorized(client):
    response = client.patch("/advertisements/1/buy")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_buy_nonexistent_advertisement(client, auth_token):
    response = client.patch(
        "/advertisements/999/buy",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_filter_advertisements_multiple_params(client, auth_token):
    form_data1 = {
        'title': 'iPhone Electronics',
        'description': 'Available phone',
        'price': '1000.00',
        'category': 'electronics'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data1
    )

    form_data2 = {
        'title': 'Chair Furniture',
        'description': 'Available chair',
        'price': '200.00',
        'category': 'furniture'
    }
    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data2
    )

    response = client.get("/advertisements/all?category=electronics&search=iPhone&status=available")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "iPhone Electronics"
    assert data[0]["category"] == "electronics"
    assert data[0]["status"] == "available"


def test_advertisement_with_maximum_photos(client, auth_token):
    form_data = {
        'title': 'Item with max photos',
        'description': 'Has maximum photos',
        'price': '500.00',
        'category': 'electronics'
    }

    files = [
        ('photos', (f'test{i}.jpg', b'fake image data', 'image/jpeg'))
        for i in range(5)
    ]

    response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data,
        files=files
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["photos"]) == 5


def test_advertisement_exceeds_photo_limit(client, auth_token):
    form_data = {
        'title': 'Item with too many photos',
        'description': 'Exceeds photo limit',
        'price': '500.00',
        'category': 'electronics'
    }

    files = [
        ('photos', (f'test{i}.jpg', b'fake image data', 'image/jpeg'))
        for i in range(6)
    ]

    response = client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data,
        files=files
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "maximum 5 photos" in response.json()["detail"].lower()


def test_search_advertisements_case_insensitive(client, auth_token):
    form_data = {
        'title': 'iPhone Pro Max',
        'description': 'Latest smartphone model',
        'price': '1200.00',
        'category': 'electronics'
    }

    client.post(
        "/advertisements/",
        headers={"Authorization": f"Bearer {auth_token}"},
        data=form_data
    )

    response = client.get("/advertisements/all?search=iphone")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1

    response = client.get("/advertisements/all?search=SMARTPHONE")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1