
from requests import delete
from graphene import relay, ObjectType, Schema, Mutation
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Category, Ingredient


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name']
        interfaces = (relay.Node, )

class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # filter_fields = ['name', 'category','notes']
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'category': ['exact'],
            'notes': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )






class CategoryMutation(Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryNode)
    @classmethod
    def mutate(cls, root, info, name):
        category = Category.objects.create(name=name)
        return CategoryMutation(category=category)

# class CategoryMutationDelete(Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)

#     category = graphene.Field(CategoryNode)
#     @classmethod
#     def mutate(cls, root, info, id):
#         category = Category.objects.get(pk=id)
#         return CategoryMutation(category=category)

class Query(ObjectType):
   category = relay.Node.Field(CategoryNode)
   all_categories = DjangoFilterConnectionField(CategoryNode)
   ingredient = relay.Node.Field(IngredientNode)
   all_ingredients = DjangoFilterConnectionField(IngredientNode)

class Mutation(graphene.ObjectType):
    create_category = CategoryMutation.Field()
    # delete_category = CategoryMutationDelete.Field()


schema = Schema(query=Query, mutation=Mutation)