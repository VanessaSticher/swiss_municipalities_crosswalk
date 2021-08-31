# swiss-municipalities-crosswalk: Crosswalk for Swiss municipalities

This package provides code to map Swiss municipality (_Gemeinde_) names across time (back to 1948). The information about the changes in names of municipalities is retrieved from the official website of the Swiss Federal Statistical Office (https://www.agvchapp.bfs.admin.ch/de/home; available in German, French, and Italian). Note that this code only maps names of municipalities over time, not borders.


## Getting Started

### Prerequisites

### Installation
Install from Github using pip:
   ```sh
   pip install https://github.com/VanessaSticher/swiss-municipalities-crosswalk/master
   ```    



## Usage

### Create file with changes

### Create custom crosswalk file
The function `swiss_municipaliy_crosswalk.create_crosswalk()` creates a custom crosswalk file for municipality names between two dates. The file can be exported to a comma-separated values file (.csv), a Stata data file (.dta), or stored as a Pandas dataframe.
#### Example
Imagine you have a dataset with historical 

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |




### Use your crosswalk file
Crosswalk file has x columns: municipality_old, municipalityYEAR, IDs?

