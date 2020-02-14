from unittest.mock import Mock

from graphql import TypeInfo, visit, ValidationContext, parse

from graphql_utilities.visitor import CostAnalysisVisitor
from tests.schema import post_schema


def describe_cost_analysis():
    on_error_stub = Mock()

    def _calculate_cost(ast_document, max_complexity=100) -> int:
        context = ValidationContext(schema=post_schema, ast=ast_document,
                                    type_info=TypeInfo(post_schema), on_error=on_error_stub)
        visitor = CostAnalysisVisitor(context=context, max_complexity=max_complexity)
        visit(ast_document, visitor)
        return visitor.total_complexity

    def test_simple_scalar_only_cost():
        document = parse("""
            query {
                announcement(id: "AAAAA") {
                    announcementId
                }
            }
        """)
        complexity = _calculate_cost(ast_document=document)
        assert complexity == 4

    def test_simple_scalar_cost():
        # Directives are not supposed to be inherited
        document = parse("""
                    query {
                        announcement(id: "AAAAA") {
                            createdAt
                            announcementId
                        }
                    }
                """)
        complexity = _calculate_cost(ast_document=document)
        assert complexity == 4

    def test_simple_cost_with_object_type():
        document = parse("""
            query {
                post(id: "XXXXXXXXXXXXXX") {
                    postId
                    title
                    author {
                        name
                    }
                }
            }
        """)
        complexity = _calculate_cost(ast_document=document)
        assert complexity == 20

    def test_overridden_cost():
        # Directives are not supposed to be inherited
        document = parse("""
            query {
                post(id: "XXXXXXXXXXXXXX") {
                    postId
                    createdAt
                    updatedAt
                }
            }
        """)
        complexity = _calculate_cost(ast_document=document)
        assert complexity == 16

    def test_multiplier_without_overriding_complexity():
        document = parse("""
            query {
                posts(first: 5) {
                    title
                    isPublic
                }
            }
        """)

        complexity = _calculate_cost(ast_document=document)
        assert complexity == 50

    def test_multiplier_with_complexity_overridden():
        document = parse("""
                    query {
                        postsWithOverride(first: 5) {
                            title
                            isPublic
                        }
                    }
                """)

        complexity = _calculate_cost(ast_document=document)
        assert complexity == 20

    def test_inline_fragment():
        document = parse("""
            query {
                postsOrAnnouncements(first: 5) {
                    ... on Post {
                        postId
                    }
                    ... on Announcement {
                        announcementId
                    }
                }
            }
        """)

        complexity = _calculate_cost(ast_document=document)
        assert complexity == 20

    def test_fragment_spread():
        document = parse("""
                    query {
                        postsOrAnnouncements(first: 5) {
                            ... postIdField
                            ... announcementIdField
                        }
                    }
                    
                    fragment announcementIdField on Announcement {
                        announcementId
                    }
                    
                    fragment postIdField on Post {
                        postId
                        createdAt
                    }
                """)

        complexity = _calculate_cost(ast_document=document)
        assert complexity == 40
