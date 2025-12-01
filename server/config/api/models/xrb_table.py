from django.db import models

# Create your models here.

class XRBTable(SQLModel, table=True):
    __tablename__ = "xrb_table"
    __table_args__ = {"schema": "public"}

    name: str = Field(
        default=None,
        sa_column=Column("Name", String)
    )

    dist: float = Field(
        default=None,
        sa_column=Column("Distance", Float)
    )

    distErr: float = Field(
        default=None,
        sa_column=Column("Distance Error", Float)
    )

    rl: str = Field(
        default=None,
        sa_column=Column("RL/RQ Flag", String)
    )
    
    incl: float = Field(
        default=None,
        sa_column=Column("Inclination", Float)
    )

    incl_err: float = Field(
        default=None,
        sa_column=Column("Inclination Error", Float)
    )

    hardline_slope: float = Field(
        default=None,
        sa_column=Column("Emission Variance (EV)", Float)
    )

    hardline_slope_err: float = Field(
        default=None,
        sa_column=Column("EV Error", Float)
    )

    spec_type: str = Field(
        default=None,
        sa_column=Column("Star Type", String)
    )

    porb: float = Field(
        default=None,
        sa_column=Column("Orbital Period", Float)
    )

    mass: float = Field(
        default=None,
        sa_column=Column("Mass", Float)
    )
