"""empty message

Revision ID: 214546816463
Revises: eb5ead75fb8f
Create Date: 2020-07-10 15:05:46.851757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '214546816463'
down_revision = 'eb5ead75fb8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###
