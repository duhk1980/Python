# Variables
$containerName = "product-catalogs"
$folderPath = "C:\Users\pc-duhk\temp\Python\Fuction\BlobTriggerToMSSQL\Upload"
$sasToken = "?sv=2018-03-28&st=2025-02-22T22%3A02%3A06Z&se=2025-02-23T22%3A02%3A06Z&sr=c&sp=racwl&sig=IEyfUeDG31rkNWDotF70ruySNl3Zna4Slgajb0ozZuY%3D"  # SAS token with appropriate permissions
$azuriteUrl = "http://127.0.0.1:10000/devstoreaccount1"

# Get all CSV files in the folder
$files = Get-ChildItem -Path $folderPath -Filter "*.csv"

foreach ($file in $files) {
    $filePath = $file.FullName
    $blobName = $file.Name
    # Construct the Blob URL with SAS Token
    $blobUrl = "$azuriteUrl/$containerName/$blobName$sasToken"

    # Detailed Logging
    Write-Host "Blob URL: $blobUrl"

    try {
        Write-Host "Uploading file: $filePath"
        # Upload the file to blob storage using SAS Token
        $result = Invoke-RestMethod -Uri $blobUrl -Method Put -InFile $filePath -Headers @{"x-ms-blob-type" = "BlockBlob"}
        Write-Host "File uploaded successfully: $blobName"
    }
    catch {
        Write-Host "Error uploading file: $filePath"
        Write-Host $_.Exception.Message
    }
}
