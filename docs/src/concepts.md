# Concepts
## Session 
Neuroscience experiments typically always come from a particular recording session. This can be explicitly defined as the time period in which an acquisition system is used to collect neural signal data from a unqiue subject. A single session can include multiple recordings, and can span but will always be assiociated with a single subject.

## Description of modality, user population

Session information is part of most data modalities. This is a minimal schema with a few number of tables describing the experiment session (data and time, experimenter, subject reference, experiment rig, aims, and, notes), the prject in which the sessions may beling to (project description, DOI, keywords, etc.),  data directory for each session.

## Precursor Projects

All DataJoint pipelines have some form of a session schema or tables. The session table is typically in the upstream part of the pipeline, referencing the subject and serves as a common node for other modalities to connect to and expand downstream (e.g. ephys, imaging, video tracking, behavioral events, optogenetic perturbation, etc.).

## Element Architecture

Each node in the following diagram represents the analysis code in the workflow for Element Session and corresponding table in the database.  Within the workflow, Element Session directly connects to upstream Element Subject, and indirectly connects to upstream schemas Project and User.

![element-session diagram](https://raw.githubusercontent.com/datajoint/element-session/main/images/session_diagram.svg)

### `subject` schema

| Table | Description |
| --- | --- |
| Subject | Basic information of the research subject |

### `session_with_datetime` schema

| Table | Description |
| --- | --- |
| Session | Stores session information with unique datetimes |
| SessionDirectory | A collection paths to data directory for a session |
| SessionExperimenter | A record of indivual(s) conducting session |
| SessionNote | Stores notes related to sessions |
| ProjectSession | Stores session information associated with a project |

### `session_with_id` schema

| Table | Description |
| --- | --- |
| Session | Stores session information using unique numerical IDs |
| SessionDirectory | A collection paths to data directory for a session |
| SessionExperimenter | A record of indivual(s) conducting session |
| SessionNote | Stores notes related to sessions |
| ProjectSession | Stores session information associated with a project |

## Element Development

We developed the Session Element under https://github.com/datajoint/element-session. This schema is validated as part of complete workflows in the specific modalities.


