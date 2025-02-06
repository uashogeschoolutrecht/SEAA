# Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; rm .\AzureCLI.msi

# Login to Azure
az login


# Create a function app
az functionapp create --resource-group RG-DataAnalytics-Sandbox --consumption-plan-location westeurope --runtime python --runtime-version 3.12 --functions-version 4 --name SEAArunner --storage-account accounttdenasandbox --os-type linux
az functionapp config appsettings set --name SEAArunner --resource-group RG-DataAnalytics-Sandbox --settings FUNCTIONS_WORKER_RUNTIME=python
# Deploy your function
func azure functionapp publish SEAArunner