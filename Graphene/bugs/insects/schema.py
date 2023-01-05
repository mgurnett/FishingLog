# # insects/schema.py
# import graphene
# from graphene_django import DjangoObjectType

# from .models import *

# class TempType(DjangoObjectType):
#     class Meta:
#         model = Temp
#         fields = '__all__'

# class BugType(DjangoObjectType):
#     class Meta:
#         model = Bug
#         fields = '__all__'

# class WeekType(DjangoObjectType):
#     class Meta:
#         model = Week
#         fields = '__all__'

# class LogType(DjangoObjectType):
#     class Meta:
#         model = Log
#         fields = '__all__'

# class HatchType(DjangoObjectType):
#     class Meta:
#         model = Hatch
#         fields = '__all__'

# class Bug_siteType(DjangoObjectType):
#     class Meta:
#         model = Bug_site
#         fields = '__all__'

# class Query(graphene.ObjectType):

#     all_logs = graphene.Field(LogType, id=graphene.Int())

#     def resolve_all_logs (root, info, id):
#         log = Log.objects.get(pk=id)
#         return Temp.objects.get(pk=log.temp.id)

# schema = graphene.Schema(query=Query) 