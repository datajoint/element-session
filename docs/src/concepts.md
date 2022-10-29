# Concepts

Neuroscience experiments typically structure a repeatable protocol around a single
recording session. A session might be explicitly defined as the time period in which an
acquisition system is used to collect neural signal data from a unique subject. A
session might include multiple recordings across data modalities or over time. Sessions
are typically limited, however, to a single subject; this assumption has been encoded in
the standard relationship between Element Animal and Element Session.

This Element is a minimal schema with relatively few tables to describe the experiment
session (e.g., data and time, experimenter, subject reference), the project in which the
sessions may belong to (e.g., DOI, keywords, etc.), and the data directory for each
session.

## Precursor Projects

All DataJoint pipelines have some form of a session schema or tables. The session table
is typically in the upstream part of the pipeline, referencing the subject and serving
as a common node to which all other modalities connect and expand downstream (e.g.
ephys, imaging, video tracking, behavioral events, etc.).

## Element Architecture

Each node in the following diagram represents the analysis code in the workflow for
Element Session and corresponding table in the database.  Within the workflow, Element
Session directly connects to upstream Element Animal, and indirectly connects to
upstream schemas Project and User.

![element-session diagram](https://raw.githubusercontent.com/datajoint/element-session/main/images/session_diagram.svg)

This Element offer two schema, which differ in how sessions are uniquely identified.
Researchers who wish to keep track of sessions based on when they occurred should use
`session_with_datetime`. Researchers wo would prefer unique integer IDs can use
`session_with_id`.

### `subject` schema

| Table | Description |
| --- | --- |
| Subject | Basic information of the research subject |

### `session` schema (APIs: [datetime](../api/element_session/session_with_datetime) or [ID](../api/element_session/session_with_id))

| Table | Description |
| --- | --- |
| Session | Stores session information with unique datetimes or numerical IDs |
| SessionDirectory | A collection paths to data directory for a session |
| SessionExperimenter | A record of individual(s) conducting session |
| SessionNote | Stores notes related to sessions |
| ProjectSession | Stores session information associated with a project |

## Roadmap

Further development of this Element is community driven. Upon user requests and based on guidance from the Scientific Steering Group we will add features to this Element.
