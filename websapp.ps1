# Create App Service Plan
az appservice plan create --name AL-webapp-test --resource-group RG-DataAnalytics-Sandbox --sku B1 --is-linux

# Create Web App
az webapp create --resource-group RG-DataAnalytics-Sandbox --plan AL-webapp-test --name AL-webapp-test --runtime "PYTHON:3.9" --startup-file "startup.txt"

# Set Python version
az webapp config set --resource-group RG-DataAnalytics-Sandbox --name AL-webapp-test --linux-fx-version "PYTHON:3.9"

# Configure continuous deployment
az webapp deployment source config-local-git --name AL-webapp-test --resource-group RG-DataAnalytics-Sandbox

# Configure environment variables
az webapp config appsettings set --resource-group RG-DataAnalytics-Sandbox --name AL-webapp-test --settings FLASK_ENV=production

# Get publishing credentials
az webapp deployment list-publishing-credentials --name AL-webapp-test --resource-group RG-DataAnalytics-Sandbox

git remote add azure https://<deployment-username>:<deployment-password>@<app-name>.scm.azurewebsites.net/<app-name>.git
# # Create required directories
# The URL will be provided in the output of the previous command
git remote add azure https://al-webapp-test.scm.azurewebsites.net:443/AL-webapp-test.git
git push azure master

$AL-webapp-test
YMZnCdt7EeiEkAP0aL8mkyYt16pFDrl4mwGAXqDyiwKZmGMoXPiA7vMNTHdX