from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    times_used = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(
        Product, 
        through='RecipeIngredient',
        related_name='recipes'
    )

    def __str__(self):
        return self.name
    
    def get_ingredients_dict(self):
        ingredients = self.recipe_ingredients.select_related('product').all()
        return {ingredient.product.name: ingredient.weight for ingredient in ingredients}


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ingredients')
    weight = models.IntegerField()

    class Meta:
        unique_together = ('recipe', 'product')

    def __str__(self):
        return f"{self.product.name} ({self.weight} г) in {self.recipe.name}"
