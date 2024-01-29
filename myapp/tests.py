from django.test import TestCase
from django.test import Client
import pytest
from django.urls import reverse
from .models import Product, Recipe, RecipeIngredient

@pytest.mark.django_db
def test_add_product_to_recipe(client):
    recipe = Recipe.objects.create(name="Test Recipe")
    product = Product.objects.create(name="Test Product")
    response = client.get(reverse('add_product_to_recipe', args=[recipe.id, product.id, 100]))
    assert response.status_code == 200
    assert RecipeIngredient.objects.filter(recipe=recipe, product=product).exists()

@pytest.mark.django_db
def test_show_recipes_without_product(client):
    product = Product.objects.create(name="Test Product")
    response = client.get(reverse('show_recipes_without_product'))
    assert response.status_code == 200
 

@pytest.mark.django_db
def test_add_product_to_recipe_with_invalid_data():
    client = Client()
    response = client.get(reverse('add_product_to_recipe', args=[999, 999, 100]))
    assert response.status_code == 404  

@pytest.mark.django_db
def test_cook_recipe_with_invalid_id():
    client = Client()
    response = client.get(reverse('cook_recipe', args=[999]))
    assert response.status_code == 404  
