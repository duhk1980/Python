# upload csv file to blobstorage using SAS
# Variables
$containerName = "product-catalogs"
$filePath = "C:\Users\pc-duhk\temp\Python\Fuction\BlobTriggerToMSSQL\upload.csv"
#$blobName = "upload.csv"
$sasToken = "?sv=2018-03-28&st=2025-02-22T22%3A02%3A06Z&se=2025-02-23T22%3A02%3A06Z&sr=c&sp=racwl&sig=IEyfUeDG31rkNWDotF70ruySNl3Zna4Slgajb0ozZuY%3D"  # SAS token with appropriate permissions
$azuriteUrl = "http://127.0.0.1:10000/devstoreaccount1"

# Construct the Blob URL with SAS Token


# Detailed Logging

$n=50
# Loop to upload the file 10 times or until break
for ($i = 1; $i -le $n; $i++) {
    # Construct the dynamic filename
    $blobName = "${i}_upload.csv"
    # Construct the Blob URL with SAS Token
    $blobUrl = "$azuriteUrl/$containerName/$blobName$sasToken"
    Write-Host "Blob URL: $blobUrl"
    try {
        Write-Host "Uploading file..."
        # Upload the file to blob storage using SAS Token
        $result = Invoke-RestMethod -Uri $blobUrl -Method Put -InFile $filePath -Headers @{"x-ms-blob-type" = "BlockBlob"}
        Write-Host "File uploaded successfully.Iteration: $i"
        # Optionally add a delay between uploads
        Start-Sleep -Seconds 10
    }
    catch {
        Write-Host "Error uploading file Iteration: $i"
        Write-Host $_.Exception.Message
        # or Break to stop
        break
    }
}