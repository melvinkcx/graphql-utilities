from typing import Union

from graphql import extend_schema, parse, Source, GraphQLSchema, build_schema as _build_schema

from graphql_utilities.directives import cost_directive_source_doc


def build_schema_with_cost(source: Union[str, Source],
                 assume_valid=False,
                 assume_valid_sdl=False,
                 no_location=False,
                 experimental_fragment_variables=False,
                 ) -> GraphQLSchema:
    schema_with_cost_directive = _build_schema(source=cost_directive_source_doc, assume_valid=assume_valid,
                                               assume_valid_sdl=assume_valid_sdl, no_location=no_location,
                                               experimental_fragment_variables=experimental_fragment_variables)
    return extend_schema(schema=schema_with_cost_directive, document_ast=parse(source), assume_valid=assume_valid,
                         assume_valid_sdl=assume_valid_sdl)
