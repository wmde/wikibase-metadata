"""Mutation"""

import strawberry

from model.strawberry.mutation_breakout import (
    ObservationMutation,
    SoftwareMutation,
    UpsertWikibaseMutation,
)


@strawberry.type
class Mutation(ObservationMutation, SoftwareMutation, UpsertWikibaseMutation):
    """Mutation"""
