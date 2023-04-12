# AGU Harvester
Goal: Harvest abstracts/papers of the AGU Fall Meeting for ingest to ADS. 
Includes documentation, Jupyter notebooks, and files for this project.

## Harvesting from AGU's API to Include as Content in ADS

Recently NASA has asked the Astrophysics Data System to develop a plan to expand its service from Astrophysics to cover all five scientific disciplines supported by NASA’s Science Mission Directorate (Heliophysics, Planetary Science, Astrophysics, Earth Science, Biophysics). The initial phase of this expansion, into Planetary Science and Heliophysics, has now been approved and funded ([Accomazzi 2021](https://ui.adsabs.harvard.edu/abs/2021AAS...23813203A/abstract)). Over the past year we developed a census to ensure research areas such as Space Science, Astrobiology, Aeronomy and Solar Physics are properly accounted for and represented in our database. The ultimate goal of this effort is to provide the same level of support for these disciplines as ADS currently provides for Astrophysics: current and accurate coverage of both refereed and gray literature, preprints, data and software. We expect that enhanced search capabilities will be developed in due time through collaborations with partners and stakeholders.

The project described in this document is aims to assess the conference proceedings of the annual AGU Fall Meeting, retrieve the abstracts' metadata, and transform the data, and curate them as individual bibliographic records in a format that can be ingested into ADS's collection. This is one example of ADS’s goal to expand partnership connections, and to increase access to scientific data and literature. The results of this project will be a step toward fulfilling ADS coverage of literature relevant in Earth and Space Sciences.

As a Librarian for Digital Technologies Development to the ADS Team supporting curation efforts and assisting in collection management, this appealed to my interests as I have been actively seeking new projects to hone my Python skills and learn new methods to curate content for the ADS. Jupyter Notebook is especially useful for beginner Python users because it helps break up scripts into more manageable blocks (cells) and notes, findings and documentation can be included along the way.
 
In this document I will outline the goals I established, the steps I took to accomplish them, and lessons learned. To accomplish this project, I used a combination of my own knowledge and expertise, read API documentation, searched the internet for solutions as needed, and collaborated with team members to debug and refine my code.

## Project Outline and Goals

The source data used in this project was retrieved from AGU's Confex API (with metadata for author names, author affiliations, author ORCIDs if available, title, abstract, and paper identifier as assigned by AGU).

The main overall goal was to write a process that could retrieve data for a specific AGU conference, and from that data, curate records for ingest into ADS. My second priority was to make this process repeatable for other conferences in the future, as necessary for expanding coverage in the ADS. I split up my overal goal into two major tasks:

1. [Task 1: Retrieve Paper and Author data from AGU API](#agu-api)
2. [Task 2: Curate data into ADS tagged records](#ads-records)

<details>
 <summary>Task 1 Details</summary>
 
## <a name="agu-api">Task 1: Retrieve Paper and Author data from AGU API</a>
  
Accomplishing this first task meant connecting to AGU's Confex API, and pulling the Paper data specific to the meeting. To access this data, I needed to make an API request to "https://agu.confex.com/agu/{meetingcode}/meetingapi.cgi/Paper". From there I was able to retrieve title, abstract, and DOI as available, however I found that I needed to look further for author names, affiliations, and ORCIDs. Upon reading the API documentation and inquiring Confex about the specifics, I discovered that I would need to also retrieve 'role' identifiers for each paper. The data for each paper points to Roles that indicate the authors' names, affiliations, ORCIDs, and the order in the author list. Therefore, I had to take additional steps to query a separate Roles path ("https://agu.confex.com/agu/{meetingcode}/meetingapi.cgi/{RoleID}") in the API to retrieve individual author metadata associated with each paper. Since the AGU API only seemed to support retrieving author data one "role" at a time, there was no option but to cycle through the entire "roles" list, one by one out of approximately 100 thousand.
  
Once I was able to retrieve both sets of data (Papers and all Role results), my next task was to merge the data and join the authors to their papers so that I could curate records.
</details>

<details>
 <summary>Task 2 Details</summary>
 
## <a name="ads-records">Task 2: Curate data into ADS tagged records</a>
  
In order to accomplish this second task, I first conducted some data cleanup and transformation. I cleaned up some HTML in the abstracts and titles, and made some transformations, such as generating the affilliations to include ORCIDs, and stringing together publication information. Then, I grouped together the authors and affiliations for each paper, and joined them to their respective papers by "PaperID".
  
Finally, I converted each metadata point to a list, and zipped them together into individual records. At that point, I was able to convert the data set to json, and run each json record through the ADS PyIngest Serializer, transforming the json records into ADS Tagged Format.
 
ADS [PyIngest](https://github.com/adsabs/adsabs-pyingest) is a collection of python parsers, validators, and serializers for the ADS Ingest Pipeline. Working with my team, I found that the PyIngest Classic Serializer gave me the best way to parse my json records and transform them into ADS Tagged Format records. It was wonderfully easy to use and helped me accomplish my goal of creating ADS Tagged records for ingest into the collection. 
  
At last, I completed my goal of curating the AGU Fall Meeting 2021 records, and sent them to our Data Ingest and Curation expert on the ADS Team for ingest.

</details>

## Version 2

[Project Notebook: AGU Harvester - VERSION 2](https://github.com/jrkoch127/agu-harvester/blob/main/AGU_Harvester-V2.ipynb)

After successfully harvesting data, transforming it, and curating the papers for ADS ingest, I went back to refine my python and make sure it would be repeatable in the future for other AGU meetings we want to ingest. Running my script again, I kept having issues with the Confex API in that it was performing too slowly when trying to retrieve the Role/Affiliation metadata. With this in mind, I created a workaround, "Version 2" that I could use in the event my original script isn't getting the data I need for future meetings. 

Version 2 is mostly unchanged from the original, except for the middle section where I connect to the Roles API. Where in the first version, I dump the role results to an excel file, in this version I save individual json files for each role. Then I will load the data into an excel sheet and resume my original process. This of course had me saving over 100K json files, but on the upside it was easier to pause and resume my API requests as needed. It took me a few days to completely obtain all the json files, but if it's performing as needed, I can easily use this as a backup plan.

## Lessons Learned

- The larger the data set, the heavier the burden on the API. This is common sense, but it really showed in this project. It gave me a better sense of what APIs can handle, depending on the insitution and rate limit (and how important a rate limit can be).
- This project gave me an opportunity to learn how to wrangle data that necessitated use of multiple API paths.
- This project also challenged me to look at multiple approaches to reaching the same goal.

## Results & Conclusions

Overall this was a great opportunity for me to learn and practice wrangling large amounts of data from APIs. It was extra helpful when I started to include print messages with timestamps, which helped me gauge how long it would take to obtain data from an API. In the future it would be great to figure out if I can write a message that tells me a metric estimate of how long the API requests will take until finished, and a running percentage. The original version lapsed about 4 hours, and Version 2 was much longer with the pausing and resuming.
