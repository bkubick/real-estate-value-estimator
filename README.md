# Real Estate Evaluator
  Brandon Kubick


### Problem to Solve
The purpose of this project consisted of two parts. The first was creating a data pipeline to generate, transform, and ingest data into a MySQL database that can be used later on as I continue this project. The second part was implementing machine learning to predict house values based off  employment and housing data. Each machine learning model was tested by combining all cities into a single regional data set or treating each city as its own independent data set. The data used in this project included housing data scraped from Homes.com and employment data grabbed from the Bureau of Labor Statistics API.

#### Important Notes:
- This entire project was created using Python 3.1.

- The cleaned and processed data is already generated and located in the data files in the zip. To analyze the machine learning, just run a jupyter notebook in the 'RealEstate' directory and run the notebook in the 'RealEstate/scripts' directory, 'PricePredictorMain.ipynb', to see the plots and results after setting up the project. Note that it takes a while to run the whole notebook and this notebook includes a significant amount of information that wasnt gone over in complete detail in the paper due to the word limit.

- If you want to run the scrapers, APIs, transformation, and database codes, be sure to follow the File setup section carefully to make sure the correct programs are downloaded and the location of all the files are in the correct spots for the code to run smoothly. The scrapers for all three cities ran a total of about 30-40 hours due to a 5s delay requirment and the real estate transformation script takes up to 15-30 minutes to run so I would avoid running these. If you want to do the whole thing from scratch, delete the files in each subdirectory of the 'RealEstate/data' directory except the population.csv. Once, done, run the following scripts in this order after setting up in the File setup section of this README file.

  - The script to run from the 'RealEstate/PropertyScrapers/PropertyScrapers/spiders' directory is:

    1. 'HomesSpiderSelenium.py': Need to run a total of three times and uncomment out the city you want to run. Name the file as mentioned later.

  - The scripts to run from the 'RealEstate/scripts' directory in order are:

    2. 'EconomicGenerationMain.py'
    3. 'RealEstateTransformationMain.py'
    4. 'EconomicTransformationMain.py'
    5. 'PricePredictorMain.ipynb'

  - The scripts to create the database are:

    6. 'TableCreation.py' : Sometimes it takes a second to work and you have to run it twice.
    7. 'InsertData.py'

1. #### File Setup
  1. The environment needed for the code to run correctly should be setup through the following commands from a terminal. If you have to copy the zip files to a new directory, start with the following command and then copy all the files from the zip folder (scripts, data, README.md, requirements.txt) into this RealEstate folder.

        $ mkdir RealEstate

  2. Now once the RealEstate directory is created, do the following in a terminal.
  
        $ pip install virtualenv

        $ cd RealEstate

        $ virtualenv env --python=python3

        $ . ./env/bin/activate

        $ pip install -r requirements.txt

   - If you want to run the scrapers, you first have to do some initial commands. Run the following command and do steps 3-5.

        $ scrapy startproject PropertyScrapers

  3. The scripts 'HomesSpiderFirst.py', 'HomesSpiderSelenium.py', and 'RealtorSpider.py' in the /RealEstate/scripts/Scrapers directory should then be moved or copied to the /RealEstate/PropertyScrapers/PropertyScrapers/spiders directory.
  4. The selenium scraper used for this project, 'HomesSpiderSelenium.py', requires a driver called chromedriver to run. Download the chromedriver corresponding to the google chrome installed on your computer at http://chromedriver.chromium.org/downloads. Download it to a directory of any choice. To run the 'HomesSpiderSelenium.py' correctly, the '__init__' function in the 'HomesSpiderSelenium.py' script must be changed to make 'self.driver' and 'self.driver2' have the location of the chromedriver on the computer using the code. For example, the location of my chromedriver is '/Users/BrandonKubick/Documents/chromedriver'.
  5. Move to the following scrapy folder to adjust some of the settings if you are going to run the 'HomesSpiderSelenium.py' scraper.

        $ cd PropertyScrapers/PropertyScrapers

        $ open settings.py

     - Once open, move to the DOWNLOAD_DELAY and set it equal to 5 and uncomment it. Once done, close the file and
     - To run the scraper 'HomesSpiderSelenium.py', first open 'HomesSpiderSelenium.py' and change end of the URL to match a city and state of choice. The codes used are commented out. Once the url is chosen, save the file and execute the command in the directory /RealEstate/PropertyScrapers/PropertyScrapers/spiders with the name of the file being 'AllCityHomes.json' where city is the city chosen. For instance, the city 'Redlands' would be named 'AllRedlandsHomes.json'

        $ scrapy crawl Homes_Selenium_Spider -o ../../../data/JSON/Unorganized/RealEstate/AllCityHomes.JSON

     - Note, if it doesn't open up two google chromes on your computer when you run the scraper, then either the chromdriver installed doesnt match that on your computer, or you dont have the correct path to it on 'self.driver' and 'self.driver2'.

  6. If you want to run the database code, some steps must first be done to correctly put the code into a database. The database uses 'MySQL Workbench'. Note, I dont know if this will work through a virtual environment and you might have to install everything onto your actual computer. To install this, do the following.

      1. Go to https://dev.mysql.com/downloads/workbench/ and download the MySQL Workbench 8.0.16 for the users computer.
      2. Go to https://dev.mysql.com/downloads/mysql/ and download the MySQL Community Server 8.0.16 for the users computer.
      3. Setup the workbench and use the password 'realestate' for the 'root' password upon setting up the MySQL Community Server. This will allow the code to create and insert data into a database without changing the password.
      4. Open the MySQL workbench and create a local instance. Name the host 'localhost'. Use the user 'root' and the password 'realestate'. This should allow all the code for the database creation and insertion to work without a problem.
  7. If steps 1-5 are executed correctly, the file schema should like the following in the RealEstate directory. /RealEstate
    - /env
      - A bunch of files set up through the virtual environment
    - /data
      - /CSV
        - /Economic
          - local_populations.csv
        - local_populations.numbers (this isnt really used i dont think)
      - /JSON
        - /Organized
          - /Economic
            - PhoenixEconomic.json
            - RedlandsEconomic.json
            - SchaumburgEconomic.json
          - /RealEstate
            - PhoenixHomes.json
            - RedlandsHomes.json
            - SchaumburgHomes.json
        - /Unorganized
          - /Economic
            - /local
              - PhoenixEconomic.json
              - RedlandsEconomic.json
              - SchaumburgEconomic.json
              - local_population.json
          - /RealEstate
            - AllPhoenixHomes.json
            - AllRedlandsHomes.json
            - AllSchaumburgHomes.json
    - /scripts
      - Constants.py
      - EconomicGenerationMain.py
      - PricePredictorMain.ipynb
      - InsertData.py
      - TableCreation.py
      - __init__.py
      - /Data_Transformation
        - EconomicTransformationMain.py
        - RealEstateTransformation.py
        - RealEstateTransformationMain.py
        - __init__.py
      - /Data_APIs
        - BLS.py
        - WorldBank.py
        - Zillow.py
        - __init__.py
      - /Machine_Learning
        - Classifiers.py
        - CombineData.py
        - DataAnalysis.py
        - DataPreprocessing.py
        - Regressors.py
        - __init__.py
      - /Scrapers (These are place in the PropertyScrapers directory but are just here so you can move them over)
        - HomesSpiderFirst.py
        - HomesSpiderSelenium.py
        - RealtorSpider.py
        - __init__.py
    - /PropertyScrapers
      - scrapy.cfg
      - /PropertyScrapers
        - __init__.py
        - items.py
        - middlewares.py
        - pipelines.py
        - settings.py
        - /spiders
          - HomesSpiderFirst.py
          - HomesSpiderSelenium.py
          - RealtorSpider.py
          - __init__.py
    - README.md
    - requirements.txt


2. #### scripts
  - ##### Constants.py
          - A program that saves the names of various constants set and used throughout the project. This includes filenames, series ids, date ranges, and other constants.

  - ##### PricePredictorMain.ipynb
          - A jupyter notebook that includes the analysis and machine learning portion of the project when developing the regression and classification models. This includes all the detailed analyses done in the paper along with plots, tables, and explanations on the values found.

  - ##### EconomicGenerationMain.py
          - A main program that uses the series and filenames listed in the constants file along with the BLS.py class to generate and export json files of employment data in reach region tested.

  - ##### Scrapers
    1. ##### HomesSpiderFirst.py
          - A class that takes in a scrapy.Spider object as its input. It has a class variables defining the name "HomeListing". It also has a class variable start_urls which starts the crawl at the realtor.com page for whichever city is uncommented. Note that this was ran for the Phoenix dataset and then Homes.com switched to javascript which required Selenium
    2. ##### HomesSpiderSelenium.py
          - A class that takes in a scrapy.Spider object as its input and uses selenium and the chromedriver to work properly. It has a class variables defining the name "Homes_Selenium_Spider". It also has a class variable start_urls which starts the crawl at the realtor.com page for whichever city is uncommented.
    3. ##### RealtorSpider.py
          - A class that takes in a scrapy.Spider object as its input. It has a class variables defining the name "RealtorListing". It also has a class variable start_urls which starts the crawl at the realtor.com page for Glendale Arizona.


  - ##### Data_APIs
    1. ##### BLS.py
          - A class that takes in series IDs, start year, and end year as inputs and will fetch that series data from the Bureau of Labor Statistics database for the given range of years. This class was used to find economic employment data for each region tested.
    2. ##### WorldBank.py
          - A class that takes in a country, indicator, and source chosen from the WorldBank database. It grab national data of any kind from the WorldBank database and export it as a JSON file. This class wasnt used for this project but was saved for future use.
    3. ##### Zillow.py
          - A class that takes in an address of a house and its zip code as inputs. These can then be used to grab features specific to that house from the Zillow API. This class wasnt used for this project but was saved for future use.

  - ##### Data_Transformation
    1. ##### EconomicTransformationMain.py
          - A main class used to combine the employment data with the population data for each region. This class is ran as a main class from the scripts folder to execute correctly.
    2. ##### RealEstateTransformation.py
          - A class used to clean the data generated from the HomesSpiderSelenium.py scraper. This class simplifies and organizes all the data, applies a house_ID, and seperates each houses data by year.
    3. ##### RealEstateTransformationMain.py
          - A main class that delcares RealEstateTransformation.py objects used to transform all the real estate data from each of the three cities tested.

  - ##### Database
    1. ##### InsertData.py
          - A class used to insert the data cleaned during the Data_Transformation phase into the database RealEstate created using TableCreation.py. This requires following the setup portion of this README.md file.
    2. ##### TableCreation.py
          - A class used to create a database a table schema for organizing the real estate and economic data into a usable database. This requires following the setup portion of this README.md file.

  - ##### Machine_Learning
    1. ##### Classifiers.py
          - A class that takes in training and testing data as an input and can be used to run various machine learning algoriths that are ran through scikit-learn. It stores the predicted data for each model in the object to be analyzed later in the code with each dataset initialized in the class.
    2. ##### CombineData.py
          - Used in the DataPreprocessing.py script to combine each city data with econ data for any number of cities and econ data. This data is then stored as a variable which can be called upon at any time to reset the data without having to run the CombineData code again.
    3. ##### DataAnalysis.py
    	    - A class used to generate features for a given data set input into the class. This includes individual feature analysis along with correlation matrices and vectors to be used with feature reduction.
    4. ##### DataPreprocessing.py
          - Runs the CombineData.py script to create a dataframe of the econ data and realestate data combined into one. Takes in the city and type of data to preprocess which can then be sent to the CombineData.py script to narrow down which data is being analyzed. This is ran to preprocess the data that was cleaned during the data transformation phase. This code can be used to feature reduce, encode, and many other preprocessing options to run on the data to make it easy to develop different models with the dataset acquired.
    5. ##### Regressors.py
          - A class that takes in training and testing data as an input and can be used to run various machine learning algoriths that are ran through scikit-learn. It stores the predicted data for each model in the object to be analyzed later in the code with each dataset initialized in the class.
