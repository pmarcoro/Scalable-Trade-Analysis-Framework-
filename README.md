# Power-BI-Python---Scalable-Trade-Analysis-Framework-

International trade has been an essential component of relations between countries for decades and a key driver of global economic growth, boosting the world economy by enabling access to products not available locally and fostering productive specialization.

In recent years, however, the international trade landscape has experienced significant changes driven by production reshoring, the creation of increasingly complex supply chains, the acceleration of digitalization and e-commerce, and a growing focus on environmental sustainability.

From a trade policy perspective, the global landscape has been increasingly shaped by rising protectionism aimed at protecting emerging or strategic domestic industries, increasing tariff revenues, enhancing economic and national security against external dependencies, or responding to unfair practices such as dumping. Trade agreements, which were traditionally multilateral, are increasingly being replaced by bilateral agreements between major trade blocs (for example, the recent EU–Mercosur Agreement).

At the business level, trade analysis is also essential not only to anticipate the impact of tariff barriers and mitigate logistical risks before they directly affect operating costs, but also to identify windows of opportunity in a global landscape characterized by uncertainty and constant change.

In this context, the analysis of trade flows becomes crucial not only to understand the trade patterns of different regions, but also to identify the strengths and weaknesses derived from those patterns, design effective trade policies, and dynamically assess their effectiveness.

The objective of this project is to build a scalable Power BI model that enables easy and flexible analysis of international trade data. Rather than focusing on a single industry, the project is designed as a scalable analytical framework in which:

- The same Power BI data model and relationships can be reused

- Different sectors can be analyzed by updating lookup tables and re-running the ETL pipeline

- Minimal changes are required to extend the analysis to new product groups

The project follows a two-layer architecture:

I) Raw data from UN Comtrade is processed ussing Python script. Data is standarized in a sector-agnostic fact table ready for direct use in Power BI.
II) Processed data is analyzed using a Power BI model.

The model follows a star schema and uses lookup tables to contextualize and filter fact data using a star-schema. 3 fact tables of different granularity allowing for flexible slicing and aggregation. 

## Lookup Tables

### UN Comtrade Lookup Tables


| Lookup Table Name                 | Description                                                    |
| --------------------------------- | -------------------------------------------------------------- |
| **Calendar Lookup**         | Standardized calendar attributes for time-based analysis.            |
| **Flow Lookup**                   | Standardized trade flow codes and labels.                      |
| **Frequency Lookup**              | Reporting frequency codes and labels.                          |
| **Quantity Lookup**               | Quantity unit codes and measurement definitions.               |
| **Partner Lookup**                | Partner country or region identifiers used in trade reporting. |
| **Reporter Lookup**               | Reporting country or region identifiers.                       |
| **Product Lookup [Full HS 2022]** | HS 2022 product codes and official descriptions.               |

### Custom Lookup Tables

| Lookup Table Name           | Description                                                                                   |
| --------------------------- | --------------------------------------------------------------------------------------------- |
| **Sector Lookup**           | Sector definitions for high-level product grouping.                                           |
| **Category Lookup**         | Category definitions within each sector.                                                      |
| **Product–Category Bridge** | Mapping HS product codes and category assignments and adding additional hierarchical attributes.|


## Data Model Overview

The Power BI data model is designed to be **sector-independent**. To enable a comprehensive analysis of each sector, three fact tables with different levels of granularity are used:

### Export Structure

This fact table focuses on analyzing the **productive specialization** of the main exporting countries within the sector. Its objectives are to:

- Define the categories that make up the analyzed sector and assess their relative importance, including subdivisions.
- Analyze how the export structure has changed over time.
- Examine the productive specialization of the leading exporting countries, including the relative share of the top *N* exporters and its evolution over time.

![Process Animation](trade-analysis/gifs/export_estructure.gif)

---

### Regional Analysis

This fact table is intended to analyze **exports and imports** for a selected subgroup of countries. The focus is on regions rather than individual products, allowing the analysis of:

- The HS subgroups in which the region records a trade surplus or deficit.
- The relative importance of main trading partners, both in exports and imports.
- The level of intra-industry trade within each subsector.

![Process Animation](trade-analysis/gifs/regional_focus.gif)
---

### Monthly Data

The monthly fact table allows for the analysis of **seasonality**, the effects of new trade policies, and recent trend changes in the analyzed sector. It also examines year-over-year changes in trade volume for the selected reference period, with variations broken down by product category a

![Process Animation](trade-analysis/gifs/monthly_data.gif)


---

## Analysis Workflow

The first step in the analysis is to define the sector of analysis and the HS product instances that compose it. Once the sector has been defined, the custom lookup tables must be updated by establishing a logical hierarchy of categories, subcategories, and product forms, at the user’s discretion.

After defining the sector, the required datasets are downloaded to perform the analysis. All dashboards rely on UN Comtrade data; however, each dashboard operates at a different level of granularity. As a result, three separate fact tables are generated.

### Downloading Instructions

#### Export Structure Dashboard
```
Year
 └── Flow [Fixed: Exports]
      └── HS Code
           └── Reporter [Selected]
                └── Partner [Fixed: World]
```

To construct the **Export Structure** processed fact table:

1. Download **yearly data** for the selected countries of analysis (for example, the top *N* exporters of the sector), selecting **“World”** in the *Partner* field and **“Exports”** in the *Flow* field. Due to tool limitations, it may be necessary to download multiple files. The reference file format is **JSON**.
2. Download **yearly aggregated export data** for each HS product instance and year. To do so, select **“All”** in the *Reporter* field and **“Reporter”** in the *Aggregated by* field.
3. Run the `add_other_countries` Python script to generate an **“Other Countries”** record based on the difference between world totals and the selected group of reporting countries. A processed JSON file is exported to the specified output folder.
4. Run the `etl_all` Python script to transform the file(s) into a format suitable for Power BI consumption.
5. Import the resulting file into Power BI as the **Export Structure** fact table.

### Regional Focus Dashboard
```
Year
 └── Flow 
      └── HS Code
           └── Reporter [Selected]
                └── Partner [Fixed: All]
```

1. Download **yearly data** for the selected countries of analysis, selecting **“All”** in the *Partner* field.
2. Run the `etl_all` Python script to transform the file(s) into a format suitable for Power BI consumption.
3. Import the resulting file into Power BI as the **Regional Focus** fact table.

### Monthly Data Dashboard
```
Year
 └── Month
      └── Flow
           └── HS Code
                └── Reporter [Selected]
                     └── Partner [Fixed: All]
```


1. Download **monthly data** for the selected countries of analysis, selecting **“All”** in the *Partner* field. The reference file format is **JSON**.
2. Run the `etl_all` Python script to transform the file(s) into a format suitable for Power BI consumption.
3. Import the resulting file into Power BI as the **Monthly Data** fact table.


## License & Data Usage Notice
This project uses UN Comtrade data under its respective licensing terms.
Raw and processed datasets are not redistributed in this repository.
This repository is intended solely for demonstration and portfolio purposes, focusing on data modeling, transformation logic, and visualization design.
