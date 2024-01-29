from urllib import request
from django.shortcuts import render
from django.db.models import F, Q, Sum
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Recipe, Product, RecipeIngredient

def add_product_to_recipe(request, recipe_id, product_id, weight):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)

    ingredient, created = RecipeIngredient.objects.update_or_create(
        recipe=recipe, product=product, defaults={'weight': weight}
    )

    return HttpResponse(f"Данный ингредиент уже есть в рецепте, вес ингредиента увеличилось на {weight} ")

def cook_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    for ingredient in recipe.ingredients.all():
        Product.objects.filter(id=ingredient.id).update(times_used=F('times_used') + 1)

    return HttpResponse("Рецепт приготовлен, использование продукта обновлено")



def show_recipes_without_product(request):
    products = Product.objects.annotate(
        total_weight=Sum('product_ingredients__weight')
    ).filter(
        Q(total_weight__lt=10) | Q(total_weight=None)
    )

    return render(request, 'myapp/show_product.html', {'products': products})




