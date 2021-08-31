# swiss-municipalities-crosswalk: Crosswalk for Swiss municipalities

This package provides code to map Swiss municipality (_Gemeinde_) names across time (back to 1948). The information about the changes in names of municipalities is retrieved from the official website of the Swiss Federal Statistical Office (https://www.agvchapp.bfs.admin.ch/de/home; available in German, French, and Italian). Note that this code only maps names of municipalities over time, not borders.


## Getting Started

### Prerequisites

### Installation
Installation from Github using pip:
   ```sh
   pip install https://github.com/VanessaSticher/swiss-municipalities-crosswalk/master
   ```    
Installation from PyPi:


## Usage

### Create file with changes

### Create custom crosswalk file
The function `swiss_municipaliy_crosswalk.create_crosswalk()` creates a custom crosswalk file for municipality names between two dates. The file can be exported to a comma-separated values file (.csv), a Stata data file (.dta), or stored as a Pandas dataframe.
#### Example
Imagine you have a dataset with Swiss municipalities in a given year, e.g. a municipality-level dataset with population on January 1, 1950:

| Municipality (in 1950) | Canton (in 1950) | Population |
| ---------------------- | -----------------|:----------:|
| Arzier                 | VD               |        ... |
| Biel (BE)              | BE               |        ... |
| Cumbels                | GR               |        ... |
| ...                    | ...              |        ... |

You can then create a crosswalk file between the municipality names on January 1, 1950 and any desired year, e.g. January 1, 2019:
   ```python
   create_crosswalk(date_from="01/01/1950", date_to=", cantons="all", output_format="csv", store_path="home/projectfolder") # export file to .csv
   crosswalk_df = create_crosswalk(date_from="01/01/1950", date_to=", cantons="all", output_format="Pandas") # file as Pandas dataframe
   
   ```
The resulting crosswalk contains the old municipality names (January 1, 1950) and the new municipality names (January 1, 2019) (and a few other variables):

| old_canton | old_municipality | new canton | new_municipality | ... |
| -----------| -----------------|:----------:| ---------------- | --- |
| VD         | Arzier           |         VD | Arzier-Le Muids  | ... |
| BE         | Biel (BE)        |         BE | Biel/Bienne      | ... |
| GR         | Cumbels          |         GR | Cumbel           | ... |
| ...        | ...              |        ... | ...              | ... |


### Future applications: add column with new municipality names to Pandas dataframe
This function is not ready yet.
