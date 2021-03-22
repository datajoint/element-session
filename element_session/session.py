import datajoint as dj
import importlib
import inspect

schema = dj.schema()


def activate(schema_name, create_schema=True, create_tables=True, linking_module=None):
    """
    activate(schema_name, create_schema=True, create_tables=True, linking_module=None)
        :param schema_name: schema name on the database server to activate the `session` element
        :param create_schema: when True (default), create schema in the database if it does not yet exist.
        :param create_tables: when True (default), create tables in the database if they do not yet exist.
        :param linking_module: a module name or a module containing the
         required dependencies to activate the `session` element:
             Upstream tables:
                + Subject: the subject for which a particular experimental session is associated with
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module),\
        "The argument 'dependency' must be a module's name or a module"

    schema.activate(schema_name, create_schema=create_schema,
                    create_tables=create_tables, add_objects=linking_module.__dict__)


@schema
class Session(dj.Manual):
    definition = """
    -> Subject
    session_datetime: datetime(3)
    """


@schema
class SessionDirectory(dj.Manual):
    definition = """
    -> Session
    ---
    session_dir: varchar(256)       # Path to the data directory for a particular session
    """


@schema
class Project(dj.Manual):
    definition = """
    -> Session
    ---
    session_dir: varchar(256)       # Path to the data directory for a particular session
    """


@schema
class Project(dj.Manual):
    definition = """
    project_name:       varchar(128)
    ---
    project_desc='':    varchar(1000) 
    """

    class Keyword(dj.Part):
        definition = """
        -> master
        keyword: varchar(32)
        """

    class Publication(dj.Part):
        definition = """
        -> master
        ---
        publication:     varchar(256)  # e.g. publication citation, link or DOI    
        """


@schema
class ProjectSession(dj.Manual):
    definition = """
    -> Project
    -> Session
    """