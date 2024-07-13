"""Add reset_password_token and reset_token_expiration columns

Revision ID: 71e81087acc0
Revises: 7db34aa89454
Create Date: 2024-04-26 00:29:09.055635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71e81087acc0'
down_revision = '7db34aa89454'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_password_token', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('reset_token_expiration', sa.DateTime(), nullable=True))
        batch_op.create_unique_constraint(None, ['reset_password_token'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('reset_token_expiration')
        batch_op.drop_column('reset_password_token')

    # ### end Alembic commands ###
