# Lease to Me web app
A webapp to find just the right retail space for your new business.

This repository links to a web app that aids,optimizes and recommends buyers of retail spaces to available rental spaces using a data driven approach. Small business owners typically face many challenging hurdles while purchasing a retail space. Many of these factors are dynamic in nature, involves market research that often expensive and time consuming and requires in depth knowledge of the local market that is only obtained by networking with a local tenant representative, which changes depending on the location and involves an overhead. 

## Visualizations:
### 1. Demographic factors:
Demographic factors are often important while looking to purchase a retail space. This pertains to whether your local community can support your business. This could be the age distribution, income distribution, race/ethnic distribution or gender distribution. It also could include the monetary expenses by industry or entertainment type. This data is pulled from the third party API Cherre, which processes public data.  
### 2. Property information:
Property information includes the square footage of the associated properties in the given area. It also includes available land spaces and other information like carpet area.
### 3. Places of interest nearby:
While buying nearby rental spaces, one can look at the symbiotic businesses in the nearby area and competition. Symbiotic business are denoted by the positive green sign and the red minus sign represents the competition. One can get a sense of the nearby by visualizing the places of interest.
## Data Engineering: 
1.Property data : This is the property listings available through Lease-to-Me. 
2.Third party data : Tax assessment or real-estate data, places_of_interest data and demographics information was obtained from Cherre API. This data was pulled using graph QL.
3.Tenant Requirement data : This data was also available through Lease-to-Me.
## Recommendation service:
Recommendation service: A scaled down version of the app at Lease-to-Me is provided here to showcase the recommendation serivce.
This allows users to fill in a survey some basic questions on the potential business/store and delivers a list of recommendations via a Suitability Score.
This builds a feature space of the all the relevant attributes (categorical for property features and numeric for places of interest distances) pertaining to a specific property listing and sends out the best listing using the Gower's distance to mediate between the various distance for the attributes. 
