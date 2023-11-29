# lss

SUMMARY

The goal is to build a "Repsly lunch suggestion system".
Repslyans need to have lunch and want to try new things. We want to have a suggestion of where to go for lunch, for each of our offices. And since we're scattered around the world, it is interesting to know if it's sunny there or if it's raining.
We want to have a list with every Repsly location in the world, and for each of them a single nearby restaurant suggestion, with average review and current weather conditions in that area. We want this list in CSV format, uploaded in the AWS S3 bucket and publicly available for download.
We have bigger plans for this service; to make it part of the initiative to bring all Repsly locations closer. For that purpose, please prepare it for the internal technical team to take over. On top of working code please provide a detailed description of the solution suitable for handover to the other team.

NOTE / DISCLAIMER

This project has certain limitations since time to create this system was limited.
At this movement to upload a file to Amazon S3 bucket manually AWS Configuration is needed - it is connected to a personal AWS account and therefore upload to AWS will fail because of nonexisting credentials and permissions.
This code offers basic functionality without catching any exceptions - since that kind of activity requires more time and in-depth analysis of the systems used in this DEMO and this time it was out of scope.

How to set local AWS configuration (and possibly change the upload directory to your own S3 bucket): https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

POSSIBLE IMPROVEMENTS

- adding catching of the exceptions
- adding more modularity
- code refinement (not keeping the file open during the code execution)
- use local credentials as a resource to communicate with AWS tier to avoid manual AWS Configuration before execution




