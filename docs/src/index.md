# Element Session

DataJoint Element for Session Management. DataJoint Elements collectively standardize
and automate data collection and analysis for neuroscience experiments.  Each Element is
a modular pipeline for data storage and processing with corresponding database
tables that can be combined with other Elements to assemble a fully functional pipeline.

Element Session features a DataJoint pipeline allowing for a standard approach for session
level organization. The Element is composed of schemas for 


runs DeepLabCut which uses image recognition machine learning models
to generate animal position estimates from consumer grade video equipment.  The Element
is composed of two schemas for storing data and running analysis:
- `train` - Manages model training
- `model` - Manages models and launches pose
estimation

Visit the [Concepts page](./concepts.md) for more information on 
session management and Element Session.  To get started with building your data pipeline visit the [Tutorials page](./tutorials.md).

![element-session diagram](https://raw.githubusercontent.com/datajoint/element-session/main/images/diagram_dlc.svg)