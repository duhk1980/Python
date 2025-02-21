$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    message = "Hello, RabbitMQ!"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:7071/api/HttpToRabbitMQ -Headers $headers -Body $body
