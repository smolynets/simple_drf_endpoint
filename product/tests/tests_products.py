import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from product.models import Product
from rest_framework import status
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def test_image():
    return SimpleUploadedFile(
        name="product/tests/second_test_product_image.png",
        content=bytes("test_content", "utf-8"),
        content_type="image/png",
    )


def test_products_list(client):
    product = Product.objects.create(
        name="test_name",
        desription="test_desription",
        number=1,
        image="product/tests/test_product_image.png",
    )
    response = client.get(reverse("product-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    for item in response.data:
        assert item["id"] == product.id
        assert item["name"] == product.name
        assert item["desription"] == product.desription
        assert item["number"] == product.number
        assert item["image"] == "http://testserver/product/tests/test_product_image.png"


def test_product_detail(client):
    product = Product.objects.create(
        name="test_name",
        desription="test_desription",
        number=1,
        image="product/tests/test_product_image.png",
    )
    Product.objects.create(
        name="test_name2",
        desription="test_desription2",
        number=2,
        image="product/tests/test_product_image.png",
    )
    response = client.get(reverse("product-detail", args=[product.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == product.id
    assert response.data["name"] == product.name
    assert response.data["desription"] == product.desription
    assert response.data["number"] == product.number
    assert response.data["image"] == "http://testserver/product/tests/test_product_image.png"


def test_product_create(client):
    product_before = Product.objects.count()
    with open("product/tests/test_product_image.png", "rb") as test_image:
        post_data = {
            "name": "test_name",
            "desription": "test_desription",
            "number": 1,
            "image": test_image,
        }
        response = client.post(reverse("product-list"), post_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == product_before + 1
    created_product = Product.objects.last()
    assert created_product.name == "test_name"
    assert created_product.desription == "test_desription"
    assert created_product.number == 1
    assert "test_product_image" in created_product.image.url


def test_product_delete(client):
    product = Product.objects.create(
        name="test_name",
        desription="test_desription",
        number=1,
        image="product/tests/test_product_image.png",
    )
    product_before = Product.objects.count()
    response = client.delete(reverse("product-detail", args=[product.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == product_before - 1


# def test_product_update(client, test_image):
#     product = Product.objects.create(
#         name="test_name",
#         desription="test_desription",
#         number=1,
#         image="product/tests/test_product_image.png",
#     )
#     product_before = Product.objects.count()
#     put_data = {
#         "name": "second_test_name",
#         "desription": "second_test_test_desription",
#         "number": 2,
#         "image": test_image,
#     }
#     response = client.put(
#         reverse("product-detail", args=[product.id]),
#         put_data=put_data,
#         content_type="multipart/form-data",
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert Product.objects.count() == product_before
#     product.refresh_from_db()
#     # TODO: check updated image
#     # assert test_image.name in product.image.url


def test_product_partitial_update(client, test_image):
    product = Product.objects.create(
        name="test_name",
        desription="test_desription",
        number=1,
        image="product/tests/test_product_image.png",
    )
    product_before = Product.objects.count()
    patch_data = {
        "image": test_image,
    }
    response = client.patch(
        reverse("product-detail", args=[product.id]),
        patch_data=patch_data,
        content_type="multipart/form-data",
    )
    assert response.status_code == status.HTTP_200_OK
    assert Product.objects.count() == product_before
    product.refresh_from_db()
    # TODO: check updated image
    # assert test_image.name in product.image.url
