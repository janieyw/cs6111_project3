# cs6111_project3
## Team

Jeffrey Yang (by2346) <br>
YeongWoo Kim (yk2920)

## File List

- `README.md`
- `INTEGRATED-DATASET.csv`
- code: `main.py`
- `example-run.txt`
    
## Run the program

This project requires Python 3.8. If you do not have Python 3.8 installed, you can download it from python.org. <br>
Next, be sure to install `pandas` by running:
```
pip install pandas
```
Once you have `pandas` installed, run the following under the project's root directory:
```
python3 main.py INTEGRATED-DATASET.csv min_sup min_conf
```

## Detailed Description
### Chosen NYC Open Data datatset
<strong>[NYPD Complaint Data Current (Year To Date)](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243/about_data)</strong>
This dataset includes all valid felony, misdemeanor, and violation crimes reported to the New York City Police Department (NYPD) for all complete quarters for this year up until now. Each record represents a criminal complaint in NYC and includes information abot the type of crime, the location and time of enforcement. In addition, information related to victim and suspect demographics is also included. The data is updated on a quarterly basis and falls under the categories of Public Safety and Police Department (NYPD).

### Procedure used to map the original dataset into `INTEGRATED-DATASET` file
#### 1. Selecting columns of interest
We began by identifying columns relevant to NYPD complaint data, focusing on those conducive to extracting association rules. Numerical columns and those with complex descriptions were deemed less useful for our analysis. Consequently, we excluded columns including 'CMPLNT_NUM' (Randomly generated persistent ID for each complaint), 'CMPLNT_FR_DT' (Exact date of occurrence for the reported event), 'X_COORD_CD' (X-coordinate for New York State Plane Coordinate System), 'Latitude' (Midblock Latitude coordinate for Global Coordinate System) and descriptive fields whose values are too lengthy to encode, such as 'LOC_OF_OCCUR_DESC' (Specific location of occurrence in or around the premises; inside, opposite of, front of, rear of) and 'PD_DESC' (Description of internal classification corresponding with PD code). We selected columns: 'BORO_NM', 'LAW_CAT_CD', 'OFNS_DESC', 'PATROL_BORO', 'PREM_TYP_DESC', 'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX', 'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX' for their potential to reveal patterns or associations.

#### 2. Filtering infrequent values
For each column in the selected subset, we removed rows that contain values occurring less than 100 times. This filtering was done to focus the analysis on more common occurrences, which are more likely to be statistically significant.

#### 3. Handling missing values
We then replaced any instances of (null) such as "(null)" with the string 'UNKNOWN'. This was done to ensure consistency in how missing data is treated and prevent misinterpretation of such values as distinct categories.

#### 4. Saving the cleaned data
Finally, we saved the cleaned data as a CSV file named `INTEGRATED-DATASET.csv`.

### Justification of our choice of NYC Open Data dataset
We chose the "NYPD Complaint Data Current (Year To Date)" dataset for two main reasons: real-life relevance and interest in public safety. Firstly, as a NYC resident and a frequent visitor ourselves, we find this dataset valuable because it contains up-to-date information on incidents reported throughout New York City. This makes it an essential resource for understanding the current context and dynamics of the city. Secondly, public safety is a significant concern in any urban setting, and this dataset provides deep insights into crime trends and specific locations. By analyzing this data, we hope to uncover interesting insights that could potentially lead to informed discussions aimed at enhancing safety across the city.

### Description of the internal design
* Data Preparation and Basket Creation:
    * `generate_baskets`: This function transforms the raw data into "baskets", each of which is a set of items, where each item represents a feature-value pair (e.g., 'BORO_NM / Manhattan').
* Basket Storage:
    * `save_baskets` and `load_baskets`: These functions handle serialization and deserialization of the baskets using Python's pickle module. This approach enhances efficiency, especially during the development phase, by allowing reuse of the generated baskets without reprocessing raw data.
* Candidate Generation:
    * `apriori_gen`: This function generates candidate itemsets (Ck) from the frequent itemsets of the previous iteration (Lk-1). The join step creates new candidates by merging itemsets that share the first k-2 items. The prune step eliminates any candidates that contain a subset not in Lk-1, ensuring that only potentially frequent candidates are considered.
* Frequent Itemset Generation:
    * `apriori`: The core Apriori algorithm is implemented here. It starts by counting each item across all baskets to form the initial set of frequent itemsets (L1). It then iteratively generates new candidate itemsets using `apriori_gen` and filters them based on support, calculated as the proportion of baskets containing the itemset.
* Association Rule Generation:
    * `get_association_rules`: This function takes the frequent itemsets and generates high-confidence rules. For each itemset with more than one item, it explores all possible rules by iterating over subsets of the itemset. The confidence of each rule is calculated and compared against a minimum confidence threshold.
* Main:
    * `main`: The main function handles command-line arguments for dynamic input of the dataset filename, minimum support, and minimum confidence. It loads or generates baskets, performs Apriori algorithm to find frequent itemsets, and then generates association rules based on these itemsets. Finally, it exports results (frequent itemsets and association rules) into a file named "output.txt".

### Command line specification of a compelling sample run
In `example-run.txt`, we use min_sup (0.01), min_conf (0.5), the command is 
```
python3 main.py "INTEGRATED-DATASET.csv" 0.01 0.5
```
We can find many intersting results from it, including:
* ['SUSP_RACE / BLACK'] => [SUSP_SEX / M] (Conf: 74.9500%, Supp: 22.7151%)<br>
This rule indicates a strong correlation between suspects identified as Black and being male.
* ['VIC_SEX / D'] => [LAW_CAT_CD / MISDEMEANOR] (Conf: 71.0719%, Supp: 11.3356%)
Victims identified with a diverse or undisclosed sex are predominantly involved in incidents classified as misdemeanors. This could highlight particular vulnerabilities or issues with how incidents involving non-binary or undisclosed gender individuals are handled or recorded.
* ['VIC_RACE / BLACK'] => [VIC_SEX / F] (Conf: 59.1140%, Supp: 14.1990%)
A significant proportion of victims who are Black are female, which may point to specific social vulnerabilities or targeted crimes. This data is crucial for developing protective services and support systems for this demographic.
* ['VIC_AGE_GROUP / 25-44'] => [VIC_SEX / F] (Conf: 53.0214%, Supp: 18.7737%)
The rule suggests that a substantial number of victims within the age group of 25-44 are female. This age and gender-specific insight can guide public safety measures and informative campaigns tailored to this demographic's needs.
* ['BORO_NM / MANHATTAN'] => [LAW_CAT_CD / MISDEMEANOR] (Conf: 52.8640%, Supp: 12.5967%)
Incidents reported in Manhattan are frequently classified as misdemeanors, potentially indicating a pattern in the types of crimes or the law enforcement response in this borough.
* ['BORO_NM / MANHATTAN'] => [PATROL_BORO / PATROL BORO MAN SOUTH] (Conf: 52.0301%, Supp: 12.3980%)
Over half of the incidents occurring in Manhattan fall under the South Manhattan Patrol's jurisdiction. This suggests a concentration of police reporting and possibly higher crime rates in this part of the borough.
* ['BORO_NM / BROOKLYN'] => [PATROL_BORO / PATROL BORO BKLYN SOUTH] (Conf: 50.4964%, Supp: 14.0658%)
Similarly, just over 50% of the incidents in Brooklyn are managed by the South Brooklyn Patrol Borough, indicating specific areas within Brooklyn that might require more focused law enforcement attention?
* ['PATROL_BORO / PATROL BORO BRONX'] => [SUSP_SEX / M] (Conf: 50.4027%, Supp: 10.9004%)
This suggests a high likelihood that suspects in the Bronx are male, which could be important for community policing strategies and crime prevention initiatives.
* ['BORO_NM / BRONX'] => [SUSP_SEX / M] (Conf: 50.4006%, Supp: 10.8999%)
This mirrors the previous rule, highlighting a consistent pattern across different patrol boroughs with a notable proportion of male suspects.
