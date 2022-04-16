# DataJoint Element - Session

DataJoint element for session management - U24 effort

+ `element-session` features a DataJoint pipeline design for session management. 

+ `element-session` is not a complete workflow by itself, but rather a modular design of tables and dependencies. 

+ `element-session` can be flexibly attached to any DataJoint workflow.

+ See the [Element Session documentation](https://elements.datajoint.org/description/session/) for the background information and development timeline.

+ For more information on the DataJoint Elements project, please visit https://elements.datajoint.org.  This work is supported by the National Institutes of Health.

## Installation
```
pip install element-session
```

If you already have an older version of ***element-session*** installed using `pip`, upgrade with
```
pip install --upgrade element-session
```


## Element usage

+ See the [workflow-calcium-imaging](https://github.com/datajoint/workflow-calcium-imaging)
 and [workflow-array-ephys](https://github.com/datajoint/workflow-array-ephys) repositories for example usages of `element-session`.

 ## Citation

+ If your work uses DataJoint and DataJoint Elements, please cite the respective Research Resource Identifiers (RRIDs) and manuscripts.

+ DataJoint for Python or MATLAB
    + Yatsenko D, Reimer J, Ecker AS, Walker EY, Sinz F, Berens P, Hoenselaar A, Cotton RJ, Siapas AS, Tolias AS. DataJoint: managing big scientific data using MATLAB or Python. bioRxiv. 2015 Jan 1:031658. doi: https://doi.org/10.1101/031658

    + DataJoint ([RRID:SCR_014543](https://scicrunch.org/resolver/SCR_014543)) - DataJoint for < Python or MATLAB > (version < enter version number >)

+ DataJoint Elements
    + Yatsenko D, Nguyen T, Shen S, Gunalan K, Turner CA, Guzman R, Sasaki M, Sitonic D, Reimer J, Walker EY, Tolias AS. DataJoint Elements: Data Workflows for Neurophysiology. bioRxiv. 2021 Jan 1. doi: https://doi.org/10.1101/2021.03.30.437358

    + DataJoint Elements ([RRID:SCR_021894](https://scicrunch.org/resolver/SCR_021894)) - Element Session (version < enter version number >)