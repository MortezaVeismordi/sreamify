import pytest
from apps.categories.models import Category


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(
        name='Gaming',
        slug='gaming',
        description='Gaming streams'
    )
    assert category.name == 'Gaming'
    assert category.slug == 'gaming'
