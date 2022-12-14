"""empty message

Revision ID: e108d68cb7e2
Revises: 
Create Date: 2022-09-10 16:05:20.429009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e108d68cb7e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('is_active', sa.SMALLINT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('is_active', sa.SMALLINT(), nullable=False),
    sa.Column('type', sa.Enum('preplay', 'foreplay', name='event_type'), server_default=sa.text("'preplay'"), nullable=False),
    sa.Column('sport', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('Pending', 'Started', 'Ended', 'Cancelled', name='status'), server_default=sa.text("'Pending'"), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('schedule_start', sa.DateTime(), nullable=False),
    sa.Column('actual_start', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sport'], ['sport.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('selection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('event', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('is_active', sa.SMALLINT(), nullable=False),
    sa.Column('outcome', sa.Enum('Unsettled', 'Void', 'Lose', 'Win', name='outcome'), server_default=sa.text("'Unsettled'"), nullable=False),
    sa.ForeignKeyConstraint(['event'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('selection')
    op.drop_table('event')
    op.drop_table('sport')
    # ### end Alembic commands ###
