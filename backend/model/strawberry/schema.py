"""Schema"""

from strawberry import Schema

from model.strawberry.mutation import Mutation
from model.strawberry.query import Query


schema = Schema(mutation=Mutation, query=Query)
