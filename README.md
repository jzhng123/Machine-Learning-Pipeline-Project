# Machine-Learning-Pipeline-Project-SP-2019

# Overview of Project 

The project is an online news popularity prediction Application. It helps editors learn the popularity of their work and displays the stats of popular online news trendings.
The Application is already ONLINE! Check out https://34.74.188.21:8111/ 
(If your computer's browser says 'Can’t connect securely to this page', please use a mobile device instead.)


# The first sprint iteration 
On top of the application in the MVP branch, we added the following features to add value.
* Model Storage 
In MVP part of the project, we have done the proof of our concept that our model was working correctly. For scalability, we decoupled the modeling service and prediction service. In this sprint iteration, we created model storage and therefore, the prediction service will be much more efficient given that the model is already built.

* Dashboard 
In MVP part of the project, we have done the proof of our concept that our predictive service is providing guidelines to editors. To help the editor generate more values from our data warehouse and service, we built a dashboard to visualize the stats of trending topics.

* Online Database 
 For the security of the data and for better performance when data size scales up, it is an excellent choice to make our database online. It also makes it easy to do the online prediction service. We created our online database using Google Cloud BigQuery service.
 
 
# Future sprint iterations
The future work will be focused on the following value added features.
* Makes the email subscription service work so user can get update from us.
* The improvement on the machine learning algorithm.
* Automatically gather the data and update the database everyday. Rerun the model every 2 or 3 days to generate updated model.
* Write a more robust web crawler that can support any website.

# Running the application
* In your environment, run server.py file and go to the link showed up, and Our main page will show up.

* Click on “Start to Explore!”, It will bring you to a page that shows links to different random online news articles’ prediction page. Please note that articles are randomly chosen. Therefore, each time you refresh the page, articles links will be different

* You can paste any web link of mashable articles to the prediction field. Our application will do web crawling for you and predict the popularity. Alternatively, you can click on any “Go Predict!” buttons on the page to predict the popularity of the article. It will take you to the prediction service page of the article. Click on “See Result” button to see the prediction result. Please note that the predictive model is running in the background so it may take a couple of seconds for the page to be ready to show the prediction result.



# How will everything communicate?
## User services:
*  Customer signs up on the website. Then we create a Customer resource
*  We tell the email service to send the welcome email
*  We tell the information service to ask user’s information, then we create an entry for that information in the database.
## Prediction Services
* User requests prediction. (Use prediction API sending a request to prediction service to train the model (training services) using the updated data (retrieving from the database).
* Store the trained model in the database. Then we predict the popularity using the stored model.
## Training Service
* Train the model and tune the parameters by retrieving data from the database.

## Evaluation Services
* Retrieve test data from the updated database and get the model from model storage to do the evaluation.

