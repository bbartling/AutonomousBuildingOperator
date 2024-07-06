# Get the login page
$response = Invoke-WebRequest -Uri "https://10.200.200.26/hui/index.html" -Headers $headers -Verbose

# Display the HTML content to inspect form fields
$response.Content