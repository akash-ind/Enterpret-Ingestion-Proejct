# Documentation:

## Flow:

<img width="705" alt="image" src="https://user-images.githubusercontent.com/52848850/216908186-94db0ff1-f246-4173-8b1a-a0fd293fa863.png">

## Get Started:

1. Install Python and Go to project Root, i.e directory where manage.py lies.
2. Run pip install -r requirements.txt
3. Run python3 manage.py makemigrations
4. Run python3 manage.py migrate
5. Run python3 manage.py runserver
6. Go to [localhost:8000/swagger](http://localhost:8000/swagger) for API documentation.
7. Please keep a note of base url /api/v1.
8. Swagger Authentication not enabled so please use Postman to hit APIs.

## Requirement Addressed:

1. Heterogenous Feedback Sources - Supported this by adding multiple sources such as, 
PlayStore, twitter, Discourse, and Intercom.
2. Push and Pull Integration model: An app can have any of two type when registering to any source.
3. Multi-Tenancy - Single Application can be used by multiple Clients
4. Transformation to a uniform internal structure - 
    1. Everything transformed to some fields that is the impact, title and description from the respective feedbacks from different sources.
    2. Meta data stored for all the feedbacks.
    3. For conversation type data supported a foreign key so that a feedback could be related to itself.
5. Idempotency - For every source and every application and feedback-id an Id is created by concatenating these fields and then for every record it is checked.
6. Multiple Feedback sources - Multiple application can be created and any application can be registered to multiple source.

### Adding a new Source:

1. New models can be added easily by Subclassing `BaseIngestion Model` and implementing the methods.
2. For Push model, we create a POST API which looks if the object exists or not and trigger the update or save method.
3. For Pull models, we take advantage of Registrations which will help us connect to the source APIs, we then transform the API data to model object and then save or update the object.

### Feedback Pull Model Implementation Details:

1. We are trying to run cron job for every application having some sources registered as pull model. 
2. We try to transform the API data to our naive model objects. 
3. We then try to save or update the data on Feedback model.

### Better implementation of the Pull model:

1. Pulling is an important part of application, we must be aware about any errors or progress. We should be using something like Airflow schedulers to run for every application and return us the successful or failed notification for every task.
2. Ingestion can be asynchronous in nature.
