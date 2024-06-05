# Functional Specification

## Project Objective
The main objective of this project is to examine the relationship between the results of the PISA study over multiple years and the education investments of various countries and to visualize insights derived from this analysis based on UI selection.

## Requirements
- Data from the PISA study across multiple years is required to analyze student performance in different countries.
- Data on education investments from various countries over the same time period is required.
- The data must be in a suitable format that can be used for analysis and visualization purposes.
- Python programming language will be utilized for data analysis and visualization.
- Pandas library will be used for data manipulation.
- Matplotlib and Seaborn libraries will be used for data visualization.
- Version management and collaboration through the use of VS Code integrated with GitHub
- Continuous progress ensured by task tracking and assignment through GitHub

## Functionalities
- Importing and merging the data from the PISA study and education investments from various countries.
- Cleaning and preprocessing the data to prepare it for analysis.
- Conducting statistical analyses to examine the relationship between PISA results and education investments.
- Developing visualizations (e.g. charts, graphs, maps) to illustrate the findings.
- Interpreting the results and deriving conclusions.

## User Story
| As a             | I want to                                                                                          | So that                                                                       
|------------------|:--------------------------------------------------------------------------------------------------:|-------------------------------------------------------------------------------
| User             | See a clear and intuitive display of PISA study results                                            | Easily access and view data for analysis and decision-making                  
|                  | and education funding data for various countries                                                   |
| User             | Select specific data points, such as PISA scores and education funding levels,                     | Customize the data view to focus on relevant variables and timeframes         
|                  | for different years and countries                                                                  |
| User             | View differente correlation between the selected variables                                         |
| User             | Have options for visual representation of the data, such as scatter plots or line graphs           | Better comprehend the relationship between variables through visualizations 
| User             | Navigate through the data and interpret the results easily with clear labels and intuitive controls| Conduct analysis efficiently and effectively                                 
| Researcher       | Analyze the relationship between funding levels and academic achievement                           | Inform educational policies and practices                                    
| Policymaker      | Understand how funding levels affect student outcomes                                              | Make informed decisions regarding education budget allocation                  
| Educator         | Gain insights into the correlation between funding and student performance                         | Improve teaching strategies and educational outcomes                         
| Student          | Utilize the UI for academic research projects or coursework focused on educational policy analysis | Enhance learning and understanding of educational trends                      
| Advocacy Groups  | Gather evidence supporting their cause and inform advocacy efforts                                 | Advocate effectively for increased education funding or policy changes        

## Quality Requirements
- The data must be accurate and up-to-date to perform accurate analyses.
- Visualizations should be well-designed and provide clear insights.
- Results should be verifiable and reproducible to ensure the validity of the analysis.

## Deliverables
- A Python script containing the code for processing the data, conducting the analysis, generating visualizations
- A report summarizing the analysis findings, conclusions, and recommendations.
- A presentation highlighting the key results and visualizations of the project.
## Datasets
Data Sources:
PISA Dataset URL:
https://pisadataexplorer.oecd.org/ide/idepisa/

Educational funding Dataset URL:
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/educ_uoe_finf01?format=TSV&compressed=true

## Libraries (Python)
- pandas
- numpy
- matplotlib
- tkinter
- request
