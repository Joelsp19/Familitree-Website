"""empty message

Revision ID: 8d6a5e796bdd
Revises: 96722e982e9c
Create Date: 2020-07-10 14:34:03.466152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d6a5e796bdd'
down_revision = '96722e982e9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'people', 'user', ['user_id'], ['id'])
    op.add_column('relationship', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'relationship', type_='foreignkey')
    op.drop_constraint(None, 'relationship', type_='foreignkey')
    op.create_foreign_key(None, 'relationship', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'relationship', type_='foreignkey')
    op.create_foreign_key(None, 'relationship', 'people', ['user_one_id'], ['id'])
    op.create_foreign_key(None, 'relationship', 'people', ['user_two_id'], ['id'])
    op.drop_column('relationship', 'user_id')
    op.drop_constraint(None, 'people', type_='foreignkey')
    op.drop_column('people', 'user_id')
    # ### end Alembic commands ###