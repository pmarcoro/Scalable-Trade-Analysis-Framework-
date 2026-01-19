# Power-BI-Python---Scalable-Trade-Analysis-Framework-

International trade has been an essential component of relations between countries for decades and a key driver of global economic growth, boosting the world economy by enabling access to products not available locally and fostering productive specialization.

In recent years, however, the international trade landscape has experienced significant changes driven by production reshoring, the creation of increasingly complex supply chains, the acceleration of digitalization and e-commerce, and a growing focus on environmental sustainability.

From a trade policy perspective, the global landscape has been increasingly shaped by rising protectionism aimed at protecting emerging or strategic domestic industries, increasing tariff revenues, enhancing economic and national security against external dependencies, or responding to unfair practices such as dumping. Trade agreements, which were traditionally multilateral, are increasingly being replaced by bilateral agreements between major trade blocs (for example, the recent EU–Mercosur Agreement).

In this context, the analysis of trade flows becomes crucial not only to understand the trade patterns of different regions, but also to identify the strengths and weaknesses derived from those patterns, design effective trade policies, and dynamically assess their effectiveness.

At the business level, trade analysis is also essential not only to anticipate the impact of tariff barriers and mitigate logistical risks before they directly affect operating costs, but also to identify windows of opportunity in a global landscape characterized by uncertainty and constant change.

The objective of this project is to build a scalable Power BI model that enables easy and flexible analysis of international trade data. Rather than focusing on a single industry, the project is designed as a scalable analytical framework in which:

- The same Power BI data model and relationships can be reused

- Different sectors can be analyzed by updating lookup tables and re-running the ETL pipeline

- Minimal changes are required to extend the analysis to new product groups

The project follows a two-layer architecture:

I) Data preparation: First, raw data from UN Comtrade is processed ussing Python script. Data is standarized in a sector-agnostic fact table ready for direct use in Power BI.
II) Data Analytics: The analytical layer is developed using a Power BI model. The model follows a star schema and uses lookup tables to contextualize and filter fact data using a star-schema. 3 fact tables of different granularity allowing for flexible slicing and aggregation. 

1. Data preparation layer (Python)

Standardizes raw UN Comtrade data into a consistent structure

Produces a sector-agnostic fact table

Prepares the data for direct use in Power BI

2. Analytical layer (Power BI)

Relies on a stable, star-schema-like model

Uses lookup tables to contextualize and filter fact data

Supports flexible slicing and aggregation

