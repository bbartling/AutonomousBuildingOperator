# Function to bypass SSL certificate validation for self-signed certificates
function Bypass-SSLValidation {
    Add-Type @"
        using System.Net;
        using System.Security.Cryptography.X509Certificates;
        public class TrustAllCertsPolicy : ICertificatePolicy {
            public bool CheckValidationResult(
                ServicePoint srvPoint, X509Certificate certificate,
                WebRequest request, int certificateProblem) {
                return true;
            }
        }
    "@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
}

# Bypass SSL validation
Bypass-SSLValidation

# Prompt the user for necessary information
$loginUrl = Read-Host "Enter the login URL"
$username = Read-Host "Enter your username"
$password = Read-Host "Enter your password" -AsSecureString

# Convert the secure string password to plain text for use in the form data
$plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

# Set the User-Agent header to mimic a browser
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Get the login page
$response = Invoke-WebRequest -Uri $loginUrl -Headers $headers -Verbose

# Display the HTML content to inspect form fields
$response.Content

# Check for WWW-Authenticate header to determine the authentication type
if ($response.Headers["WWW-Authenticate"]) {
    $authType = $response.Headers["WWW-Authenticate"]
    Write-Host "Authentication type detected: $authType"
} else {
    Write-Host "No WWW-Authenticate header found. This may indicate form-based or session-based authentication."
}

# Define the form fields based on inspection of the HTML content
$formData = @{
    userid   = $username
    password = $plainPassword
}

# Create a session to maintain cookies
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# Send the POST request to log in
$response = Invoke-WebRequest -Uri $loginUrl -Method Post -WebSession $session -Body $formData -Headers $headers -Verbose

# Check the response
if ($response.StatusCode -eq 200) {
    Write-Host "Login successful."
} else {
    Write-Host "Login failed. Status code: $($response.StatusCode)"
}

# Display the response body for more details
Write-Host "Response body:"
$response.Content

# Access the main protected page using the authenticated session
$protectedPageUrl = Read-Host "Enter the URL of the protected page you want to access"
$protectedResponse = Invoke-WebRequest -Uri $protectedPageUrl -WebSession $session -Headers $headers -Verbose

# Check the response for the protected page
if ($protectedResponse.StatusCode -eq 200) {
    Write-Host "Access to protected page successful."
} else {
    Write-Host "Failed to access protected page. Status code: $($protectedResponse.StatusCode)"
}

# Display the content of the protected page
$protectedResponse.Content
