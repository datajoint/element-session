import datajoint as dj
import importlib
import inspect

schema = dj.schema()
_linking_module = None


def activate(
    schema_name,
    create_schema: bool = True,
    create_tables: bool = True,
    linking_module: str = None,
):
    """Activate this schema.

    Args:
        schema_name (str): schema name on the database server
        create_schema (bool): when True (default), create schema in the database if it
                            does not yet exist.
        create_tables (str): when True (default), create schema tables in the database
                             if they do not yet exist.
        linking_module (str): a module (or name) containing the required dependencies.

    Dependencies:
    Upstream tables:
        Subject: the subject with which an experimental session is associated
        Project: the project with which experimental sessions are associated
        Experimenter: the experimenter(s) participating in a given session
                      To supply from element-lab add `Experimenter = lab.User`
                      to your `workflow/pipeline.py` before `session.activate()`
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(
        linking_module
    ), "The argument 'dependency' must be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=linking_module.__dict__,
    )


@schema
class Session(dj.Manual):
    """Central Session table

    Attributes:
        Subject (foreign key): Key for Subject table
        session_id (int): Unique numeric session ID
        session_datetime (datetime): date and time of the session
    """

    definition = """
    -> Subject
    session_id: int
    ---
    session_datetime: datetime
    """

    class Attribute(dj.Part):
        """Additional feature of interest for a session.

        Attributes:
            Session (foreign key): Key for Session table
            attribute_name ( varchar(32) ): Name shared across instances of attribute
            attribute_value ( varchar(2000), optional ):  Attribute value
            attribute_blob (longblob, optional): Optional data store field
        """

        definition = """
        -> master
        attribute_name: varchar(32)
        ---
        attribute_value='': varchar(2000)
        attribute_blob=null: longblob
        """


@schema
class SessionDirectory(dj.Manual):
    """Relative path information for files related to a given session.

    Attributes:
        Session (foreign key): Key for Session table
        session_dir ( varchar(256) ): Path to the data directory for a session
    """

    definition = """
    -> Session
    ---
    session_dir: varchar(256) # Path to the data directory for a session
    """


@schema
class SessionExperimenter(dj.Manual):
    """Individual(s) conducting the session

    Attributes:
        Session (foreign key): Key for Session table
        Experimenter (foreign key): Key for Experimenter table
    """

    definition = """
    # Individual(s) conducting the session
    -> Session
    -> Experimenter
    """


@schema
class SessionNote(dj.Manual):
    """Additional notes related to a given session

    Attributes:
        Session (foreign key): Key for Session table
        session_note ( varchar(1024) ): : Additional notes
    """

    definition = """
    -> Session
    ---
    session_note: varchar(1024)
    """


@schema
class ProjectSession(dj.Manual):
    """Table linking upstream Projects with Session

    Attributes:
        Project (foreign key): Key for Project table
        Session (foreign key): Key for Session table
    """

    definition = """
    -> Project
    -> Session
    """
