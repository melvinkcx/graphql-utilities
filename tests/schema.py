from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString, GraphQLInt

from graphql_utilities import build_schema_with_cost

schema = GraphQLSchema(
    query=GraphQLObjectType(
        name='RootQueryType',
        fields={
            'field_1_str': GraphQLField(
                GraphQLString,
                resolve=lambda obj, info: 'str_1_field'),
            'field_2_int': GraphQLField(
                GraphQLInt,
                resolve=lambda obj, info: 2),
            'field_3_obj': GraphQLField(
                GraphQLObjectType(
                    name='Field3Object',
                    fields={
                        'field_3_obj_sub_1': GraphQLField(GraphQLObjectType(
                            name='Field3ObjectSubfield1',
                            fields={
                                'xxx': GraphQLField(GraphQLString)
                            }
                        ))
                    }
                ),
                resolve=lambda obj, info: {'field_3_obj': {'field_3_obj_sub_1': '1_sub_obj_3_field'}}
            ),
            'cat': GraphQLField(
                GraphQLObjectType(
                    name='CatObject',
                    fields={
                        'meow': GraphQLField(GraphQLString)
                    },
                ),
                resolve=lambda obj, info: {"meow": "woem"}
            )
        }))

post_schema = build_schema_with_cost("""
type Author @cost(complexity: 4) {
    uid: String!
    name: String @cost(complexity: 2)
    email: String @cost(complexity: 2)
}

interface TimestampedType {
    createdAt: String @cost(complexity: 2)
    updatedAt: String @cost(complexity: 2)
}

type Post implements TimestampedType @cost(complexity: 8) {
    author: Author
    postId: String! @cost(complexity: 4)
    title: String @cost(complexity: 2)
    text: String @cost(complexity: 1)
    publishedAt: String @cost(complexity: 1)
    isPublic: Boolean  # NO cost
    createdAt: String @cost(complexity: 4) # OVERRIDE cost
    updatedAt: String
}

type Announcement implements TimestampedType {
    createdAt: String
    updatedAt: String
    announcementId: String! @cost(complexity: 4)
    title: String
    text: String
}

union PostOrAnnouncement = Post | Announcement

type Query {
    posts(first: Int): [Post]  @cost(multipliers: ["first"])
    postsWithOverride(first: Int): [Post]  @cost(complexity: 2, multipliers: ["first"]) # OVERRIDE complexity of Post type
    postsOrAnnouncements(first: Int): [PostOrAnnouncement] @cost(multipliers: ["first"])
    post(id: ID!): Post
    announcement(id: ID!): Announcement
}
""")
