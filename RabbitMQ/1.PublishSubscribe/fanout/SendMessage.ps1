# Change the working directory to the folder containing the scripts
#Set-Location "C:\Users\pc-duhk\temp\Python\0.WorkQueues"
$messageBody = "Hello world"
for ($i = 1; $i -le 100; $i++) {
    # Concatenate strings using string interpolation
    $combinedMessage = "Sent$i $messageBody"
    #echo $combinedMessage
    
    # Call the Python script with the combined message
    python .\emit_log.py $combinedMessage

    # Output the message to the console
    Write-Host "Message $i sent"

    # Simulate a break condition (e.g., based on some criteria)
    if ($i -eq 50) {
        Write-Host "Breaking the loop after 50 iterations."
        break
    }
    # Optional: Add a delay to make it easier to stop the script with Ctrl+C
    Start-Sleep -Seconds 1
}

Write-Host "Finished looping."
