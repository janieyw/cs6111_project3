# cs6111_project3
### Team

Jeffrey Yang (by2346) <br>
YeongWoo Kim (yk2920)

### Files Submitting

- README.md
- INTEGRATED-DATASET.csv
- main.py
- example-run.txt
  
### Chosen NYC Open Data datatset
<strong>[NYPD Complaint Data Current (Year To Date)](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243/about_data)</strong>
This dataset includes all valid felony, misdemeanor, and violation crimes reported to the New York City Police Department (NYPD) for all complete quarters for this year up until now. Each record represents a criminal complaint in NYC and includes information abot the type of crime, the location and time of enforcement. In addition, information related to victim and suspect demographics is also included.  The data is updated on a quarterly basis and falls under the categories of Public Safety and Police Department (NYPD).

### Procedure used to map the original dataset into `INTEGRATED-DATASET` file
#### 1. Selecting columns of interest
We began by identifying columns relevant to NYPD complaint data, focusing on those conducive to extracting association rules. Numerical columns and those with complex descriptions were deemed less useful for our analysis. Consequently, we excluded columns including 'CMPLNT_NUM' (Randomly generated persistent ID for each complaint), 'CMPLNT_FR_DT' (Exact date of occurrence for the reported event), 'X_COORD_CD' (X-coordinate for New York State Plane Coordinate System), 'Latitude' (Midblock Latitude coordinate for Global Coordinate System) and descriptive fields whose values are too lengthy to encode, such as 'LOC_OF_OCCUR_DESC' (Specific location of occurrence in or around the premises; inside, opposite of, front of, rear of) and 'PD_DESC' (Description of internal classification corresponding with PD code). We selected columns:'BORO_NM', 'LAW_CAT_CD', 'OFNS_DESC', 'PATROL_BORO', 'PREM_TYP_DESC', 'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX', 'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX' for their potential to reveal patterns or associations.

#### 2. Filtering infrequent values
For each column in the selected subset, we removed rows that contain values occurring less than 100 times. This filtering was done to focus the analysis on more common occurrences, which are more likely to be statistically significant.

#### 3. Handling missing values
We then replaced any instances of (null) such as "(null)" with the string 'UNKNOWN'. This was done to ensure consistency in how missing data is treated and prevent misinterpretation of such values as distinct categories.

#### 4. Saving the cleaned data
Finally, we saved the cleaned data as a CSV file named `INTEGRATED-DATASET.csv`.
