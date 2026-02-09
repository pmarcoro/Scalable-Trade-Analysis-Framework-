# Power-BI-Python---Scalable-Trade-Analysis-Framework-

## Overview

International trade has been an essential component of relations between countries for decades and a key driver of global economic growth, boosting the world economy by enabling access to products not available locally and fostering productive specialization.

In recent years, however, the international trade landscape has experienced significant changes driven by production reshoring, the creation of increasingly complex supply chains, the acceleration of digitalization and e-commerce, and a growing focus on environmental sustainability.

From a trade policy perspective, the global landscape has been increasingly shaped by rising protectionism aimed at protecting emerging or strategic domestic industries, increasing tariff revenues, enhancing economic and national security against external dependencies, or responding to unfair practices such as dumping. Trade agreements, which were traditionally multilateral, are increasingly being replaced by bilateral agreements between major trade blocs.

At the business level, trade analysis is also essential not only to anticipate the impact of tariff barriers and mitigate logistical risks before they directly affect operating costs, but also to identify windows of opportunity in a global landscape characterized by uncertainty and constant change.

In this context, the analysis of trade flows becomes crucial not only to understand the trade patterns of different regions, but also to identify the strengths and weaknesses derived from those patterns, design effective trade policies, and dynamically assess their effectiveness.

## Objective

The objective of this project is to build a scalable Power BI model that enables easy and flexible analysis of international trade data. Rather than focusing on a single industry, the project is designed as a scalable analytical framework in which:

- The same Power BI data model and relationships can be reused

- Different sectors can be analyzed by updating lookup tables and re-running the ETL pipeline

- Minimal changes are required to extend the analysis to new product groups

The project follows a two-layer architecture:

   1) Raw data from UN Comtrade is processed ussing Python script. Data is standarized in a sector-agnostic fact table ready for direct use in Power BI.

   2)  Processed data is analyzed using a Power BI model.

## Data Source

This project is based on international trade data sourced from [**UN Comtrade**](https://comtradeplus.un.org/), the United Nations’ official repository for global merchandise trade statistics. UN Comtrade is one of the most comprehensive and widely used sources of data on international trade flows, offering in dept product trade information based on the Harmonized System (HS) of global product classification. This system comprises more than 5,000 commodity groups, each of them identified by a 6-digit code and arranged according to a legal and logical structure.

Due to licensing and redistribution restrictions, **raw UN Comtrade data files are not included in this repository**. Users interested in using the present framework can do so downloading the data directly from the UN Comtrade platform, subject to its terms of use.

## Dashboard Preview

The Power BI model is designed to be sector-independent, allowing the same analytical framework to be reused across different industries and product groupings. 

Several interactive report pages have been developed to explore international trade flows from complementary analytical perspectives. Each page is built on a dedicated data structure and is optimized for a specific type of analysis, ranging from long-term structural patterns to short-term dynamics. Together, they provide a comprehensive view of trade specialization, regional integration, and temporal evolution within the selected sector.

---

### Export Structure Page

The Export Structure page focuses on analyzing the **productive and export specialization** of the main exporting countries within the selected sector.

Objectives:

- Define the product categories that make up the analyzed sector, including internal subdivisions, and assess their relative importance.
- Analyze how the export composition of the sector has evolved over time.
- Examine the degree of export concentration by identifying the leading exporting countries, the relative share of the top *N* exporters, and how this concentration changes over time.




<p align="center">
Export Structure Page Preview
</p>

<p align="center">
<img src="/images/gifs/Export%20Estructure%20preview.gif" width="900">
</p>

---

### Regional Analysis Page

The Regional Analysis page is designed to examine **exports and imports** for a selected group of countries or regions. The aim is to emphasizes the analysis of regional dynamics and integration patterns.

Objectives:

- Identifying HS product groups in which the selected region records persistent trade surpluses or deficits.
- Assessing the relative importance of main trading partners on both the export and import sides.
- Measuring the degree of intra-industry trade within each commodity group, providing insights into regional value chain integration.

  

<p align="center">
Regional Analysis Page Preview
</p>

<p align="center">
<img src="/images/gifs/Region%20Focus%20preview.gif" width="900">
</p>

---

### Monthly Data Page

The Monthly Data page enables higher-frequency analysis of trade flows, making it especially suitable for detecting **short-term dynamics** that are not visible in annual data.

Objectives:

- Analyzing seasonal patterns in trade volumes.
- Assessing the short-term impact of new trade policies, tariffs, or external shocks.
- Identifying recent trend changes and potential turning points in the sector.
- Comparing year-over-year changes for specific periods, broken down by HS commodity groups.
- Supporting near-real-time monitoring of trade developments for policy or market analysis.


<p align="center">
Monthly Data Page Preview
</p>

<p align="center">   
<img src="/images/gifs/Monthly%20data%20preview.gif" width="900">
</p>

## Data Processing Approach

The project follows a simplified Medallion Architecture (Bronze–Silver–Gold) logic to structure the data transformation workflow.

### Bronze Layer — Raw UN Comtrade Data
The raw JSON files downloaded from UN Comtrade represent the Bronze layer of the project. These files contain:

 - Transactional trade values
 - Reporter and partner identifiers 
 - Commodity classifications
 - Flow information
 - Metadata and auxiliary reference fields

### Silver Layer — Processed Analytical Dataset
Using custom Python scripts (etl.py, add_other_countries.py) the raw JSON files are transformed into a structured fact tables, suitable for analytical modeling.The transformation process includes:

- Selecting only columns relevant for analytical purposes
- Removing metadata fields not required for modeling
- Excluding descriptive fields that are later linked through dedicated lookup tables (to avoid redundancy and ensure normalization)
- Standardizing and renaming selected columns for clarity and consistency

### Gold Layer — Power BI model
The Gold layer corresponds to the Power BI data model, where:

 - Fact tables are connected to normalized lookup tables
 - Relationships are defined
 - Measures (DAX) are implemented
 - Business logic is applied


## Data Model

### Schema Overview
The data model is organized as a Star Schema, with a central set of fact tables connected to multiple lookup (dimension) tables. Each fact table represents a specific analytical layer (Export Structure, Regional Focus, Monthly Data) and links to the relevant dimensions such as Reporter, Partner, HS Code, Flow, and Time.

Below is a visual overview of the schema.

<p align="center">
<img src="/images/schema_overview.png" width="900">
</p>


### Fact Tables
The analytical model is structured around three core fact tables, each designed to support a specific report page and analytical perspective. Although all tables originate from UN Comtrade data, they differ in granularity, aggregation logic, and methodological treatment.


Fact Tables Overview

| Fact Table       | Time Granularity | Product Level | Reporter Scope     | Partner Scope | Flow Scope      |
| ---------------- | ---------------- | ------------- | ------------------ | ------------- | --------------- |
| Export Structure | Yearly           | HS Code       | Selected + “Other” | World         | EXP             |
| Regional Focus   | Yearly           | HS Code       | Selected           | All           | EXP & IMP       |
| Monthly Data     | Monthly          | HS Code       | Selected           | All           | EXP & IMP       |



After processing, the dataset retains the following standardized columns. The structure is common for the three fact tables.

Fact Table structure (Silver Layer)

| Column name         | Description |
|--------------------|-------------|
| `freqCode`         | Frequency of the data (e.g. annual, monthly) |
| `year`             | Calendar year of the observation |
| `period`           | Reporting period within the year with MMYYYY format |
| `hs4`              | Harmonized System (HS) product code |
| `reporterCode`     | Numeric code identifying the reporting country or economy |
| `flowCode`         | Trade flow indicator (e.g. exports or imports) |
| `partnerCode`      | Numeric code identifying the partner country or region |
| `aggrLevel`        | Level of product aggregation in the HS classification |
| `qtyUnitCode`      | Unit of measurement for reported quantities |
| `qty`              | Reported trade quantity |
| `cifvalue`         | Trade value on a CIF (Cost, Insurance, and Freight) basis |
| `fobvalue`         | Trade value on a FOB (Free On Board) basis |
| `trade_value_usd`  | Standardized trade value expressed in US dollars |
| `isAggregate`      | Boolean flag indicating whether the record corresponds to an aggregate (e.g. regional or global total) |


### Lookup Tables

The model uses various lookup tables to contextualize and filter the fact tables. These tables provide descriptive metadata, classification mappings and analytical hierarchies that are separated from the main fact table to avoid redundancy and improve model efficiency.

#### UN Comtrade Lookup Tables

Some of the lookup tables are downloaded from **UN Comtrade** and contain official reference data used to decode the raw trade records. The tables provided in the project are modified versions of such tables that add instances and contain minor modifications (e.g. "Other countries" as possible reporter).

UN Comtrade Lookup Tables Overview

| Lookup Table Name                 | Description                                                    |
| --------------------------------- | -------------------------------------------------------------- |
| **Flow Lookup**                   | Standardized trade flow codes and labels.                      |
| **Frequency Lookup**              | Reporting frequency codes and labels.                          |
| **Quantity Lookup**               | Quantity unit codes and measurement definitions.               |
| **Partner Lookup**                | Partner country or region identifiers used in trade reporting. |
| **Reporter Lookup**               | Reporting country or region identifiers.                       |
| **Product Lookup [Full HS 2022]** | HS 2022 product codes and official descriptions.               |


#### Custom Lookup Tables

In addition to the official lookups, the project includes **custom lookup tables** that must be maintained and adapted by the user. These tables are designed to:
- Link analytical **sectors** to specific HS product codes or HS instances
- Define **custom hierarchies** within each HS instance
- Enable flexible aggregation and comparison across product groups

By modifying these custom lookup tables, users can tailor the analytical structure to their specific use case.

Custom Lookup Tables Overview

| Lookup Table Name           | Description                                                                                   |
| --------------------------- | --------------------------------------------------------------------------------------------- |
| **Calendar Lookup**         | Standardized calendar attributes for time-based analysis.                                     |
| **Sector Lookup**           | Sector definitions for high-level product grouping.                                           |
| **Category Lookup**         | Category definitions within each sector.                                                      |
| **Product–Category Bridge** | Mapping HS product codes and category assignments and adding additional hierarchical attributes.|

### Measures
The analytical model leverages a set of DAX measures to perform key calculations and aggregations across the fact tables. These measures include totals, averages, and ratios that support the reporting requirements of each dashboard page.

Below is a visual overview of the measures implemented in the model.

<p align="center">
<img src="/images/measures/Measures%20image.png" width="900">
</p>


## Analytical Setup and Data Workflow

### Defining the Analytical Scope
The first step of the analysis is the definition of the sector under study. Once the relevant HS codes have been identified, the user must update the **custom lookup tables** to:
- Associate each HS instance with a sector.
- Define a logical hierarchy of categories, subcategories, and product forms.
- Adapt the analytical structure of the HS entries to improve clarity and simplify visual analysis.

This approach provides full flexibility in how sectors are defined and analyzed, while keeping the underlying trade data unchanged.

### Data Processing Pipeline
A set of custom Python scripts is used to transform raw UN Comtrade data into a standardized, reusable data model compatible with Power BI.

Because UN Comtrade CSV files frequently present encoding and parsing issues, JSON is adopted as the default raw data format. The data processing pipeline is implemented through two Python scripts:

#### 1. `etl`
This script ingests the raw JSON files, renames columns according to the target data schema and consolidates multiple source files into a single unified dataset. The processed data is then exported to Parquet format, enabling more efficient storage and compression. The standardized structure is common for each of the 3 fact tables used in the model.

#### 2. `add_other_countries`
This script is used to support the Export Structure page. Its purpose is to analyze the extent to which total exports are concentrated within a limited set of countries and to improve visual clarity by introducing an aggregated “Other countries” reporter category.

To achieve this, the script computes total exports aggregated across all countries by year, HS classification, and trade flow (exports). These totals are then compared against the aggregated value of the selected regional group. The difference between the global aggregate and the selected region constitutes the “Other countries” category.

To ensure methodological consistency, regional groupings that aggregate multiple countries (such as the European Union) must be excluded, as their inclusion would omit intra-regional trade flows and distort the results.

### Raw Data Download Instructions

All report pages rely on UN Comtrade data, but each requires a different data extraction strategy due to differences in granularity and analytical focus.

#### Export Structure Fact Table
```
Year
 └── Flow [Fixed: Exports]
      └── HS Code
           └── Reporter [Selected]
                └── Partner [Fixed: World]
```

To construct the **Export Structure** processed fact table:

1. Download **yearly data** for the selected countries of analysis / reporters (for example, the top *N* exporters of the sector in a given period), selecting **“World”** in the *Partner* field and **“Exports”** in the *Flow* field. Due to tool limitations, the number of HS commodity entries is limited to 10 per download for free users, so it may be necessary to download multiple files. Locate the JSON file(s) in the data\raw\export structure folder and rename them including the word "detailed" for them to be correctly classified by the Python script.
2. Download **yearly aggregated export data** for each HS product instance and year. To do so, select **“All”** in the *Reporter* field and **“Reporter”** in the *Aggregated by* field. Locate the JSON files in the `data/raw/export structure` folder and rename them including the word "world" for them to be detected by the Python script.
3. Run the `add_other_countries` Python script to generate an **“Other Countries”** record based on the difference between world totals and the selected group of reporting countries. A processed JSON file will be exported to `data\raw`.
4. Run the `etl` Python script to transform the resultant file into a format suitable for Power BI consumption. A Parquet file with the processed data will be created in the `data\processed` folder
5. Import the resulting file into Power BI as the **Export Structure** fact table.

* The top N countries by value of the selected sector in a given year can be identified selecting all the HS codes identifying the sector, "All" in the *Reporter* field, **“World”** in the *Partner* field and **“Exports”** in the *Flow* field, then ordering by value in the "preview". 

#### Regional Focus Fact Table
```
Year
 └── Flow 
      └── HS Code
           └── Reporter [Selected]
                └── Partner [Fixed: All]
```

1. Download **yearly data** for the desired countries of analysis (reporters), selecting **“All”** in the *Partner* field. Repeat the process for the required HS entries, downloading various files if necessary. Download the file(s) in JSON format and locate them in `data\raw`.
2. Run the `etl` Python script to transform the file(s) into a format suitable for Power BI consumption. A Parquet file with the processed data will be created in the `data\processed` folder
3. Import the resulting file into Power BI as the **Region Focus** fact table.

#### Monthly Data Fact Table
```
Year
 └── Month
      └── Flow
           └── HS Code
                └── Reporter [Selected]
                     └── Partner [Fixed: All]
```


1. Download **monthly data** for the selected countries of analysis (reporters), selecting **“All”** in the *Partner* field and the month(s) of reference desired. Locate the JSON file(s) in `data\raw`
2. Run the `etl` Python script to transform the file(s) into a format suitable for Power BI consumption.  A Parquet file with the processed data will be created in the `data\processed` folder
3. Import the resulting file into Power BI as the **Monthly Data** fact table.


## License & Data Usage Notice
UN Comtrade data is publicly available under its respective terms of use and licensing conditions as defined by the United Nations Statistics Division (UNSD). Users are responsible for complying with the official UN Comtrade data usage policies when accessing or using the data independently.

To comply with these terms:

- Raw datasets are not redistributed in this repository.
- Processed datasets are not shared in this repository.

This repository is intended for educational, demonstration, and portfolio purposes only.
