<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
<?php
/**
 * ============================================================================
 * SHENRON v3.0 - API Proxy for VM150
 * ============================================================================
 * Routes web UI requests to SHENRON API Server on VM100:5000
 * Replaces direct LM Studio fighter queries with unified SHENRON endpoint
 * ============================================================================
 */

// CORS Headers
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Configuration
$SHENRON_API = "http://<VM100_IP>:5000/api/shenron/grant-wish";

// Set generous timeouts for complex queries
set_time_limit(1800); // 30 minutes
ini_set('max_execution_time', '1800');
ini_set('memory_limit', '512M');

// Get request body
$requestBody = file_get_contents('php://input');
$requestData = json_decode($requestBody, true);

// Validate request
if (!isset($requestData['query'])) {
    http_response_code(400);
    echo json_encode([
        'error' => 'Missing query field in request',
        'wish_granted' => false
    ]);
    exit;
}

// Prepare request for SHENRON
$shenronRequest = [
    'query' => $requestData['query'],
    'use_rag' => isset($requestData['use_rag']) ? $requestData['use_rag'] : true
];

// Forward to SHENRON API Server
$ch = curl_init($SHENRON_API);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($shenronRequest));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_TIMEOUT, 1800); // 30 minutes
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);

if (curl_errno($ch)) {
    http_response_code(500);
    echo json_encode([
        'error' => 'SHENRON API connection failed: ' . $curlError,
        'wish_granted' => false,
        'debug' => [
            'shenron_api' => $SHENRON_API,
            'curl_error' => $curlError
        ]
    ]);
    curl_close($ch);
    exit;
}

curl_close($ch);

// Return SHENRON's response
http_response_code($httpCode);
echo $response;
?>

