"""Initial public

Revision ID: d6ba8c13303e
Revises: 
Create Date: 2022-07-18 15:09:21.528588

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d6ba8c13303e"
down_revision = None
branch_labels = None
depends_on = None

# op.execute("DROP SCHEMA IF EXISTS test_00000000000000000000000000000000;")
# op.execute("CREATE SCHEMA IF NOT EXISTS test_00000000000000000000000000000000;")


def upgrade() -> None:
    # tenants_statement = """
    #  CREATE TABLE IF NOT EXISTS public.tenants (
    #     id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    #     uuid uuid UNIQUE,
    #     name varchar(256) UNIQUE,
    #     schema varchar(256) UNIQUE,
    #     schema_header_id varchar(256) UNIQUE
    #     );

    #  """
    # op.execute(tenants_statement)

    public_users = """
    CREATE TABLE IF NOT EXISTS public.public_users (
       id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
       uuid uuid UNIQUE,
       email varchar(256) UNIQUE,
       password varchar(256),
       service_token varchar(256),
       service_token_valid_to TIMESTAMPTZ,
       is_active BOOLEAN NOT NULL,
       is_verified BOOLEAN NOT NULL,
       tos BOOLEAN NOT NULL,
       tenant_id varchar(64),
       tz varchar(64),
       lang varchar(8),
       created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       updated_at TIMESTAMPTZ
      );
    """
    op.execute(public_users)

    public_companies = """
    CREATE TABLE IF NOT EXISTS public.public_companies (
       id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
       uuid uuid UNIQUE,
       name varchar(256),
       short_name varchar(256),
       nip varchar(16),
       country varchar(128),
       city varchar(128),
       tenant_id varchar(64) UNIQUE,
       host varchar(64) UNIQUE,
       qr_id varchar(32) UNIQUE,
       created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
       updated_at TIMESTAMPTZ
      );
    """
    op.execute(public_companies)

    # query = sa.text("INSERT INTO public.tenants (name, schema, host) " "VALUES (:name, :schema, :host)").bindparams(
    #     name="default", schema="tenant_default", schema_header_id="127.0.0.1"
    # )
    # op.execute(query)


def downgrade() -> None:
    # op.execute("DROP TABLE IF EXISTS public.public_users CASCADE;")
    # op.execute("DROP TABLE IF EXISTS public.tenants CASCADE;")
    # op.execute("DROP SCHEMA IF EXISTS public;")
    pass
