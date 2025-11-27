<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
<?php

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    exit;
}

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$body = file_get_contents('php://input');
$input = json_decode($body, true);
if (!is_array($input)) {
    $input = [];
}

$action = $input['action'] ?? null;
$backendBase = 'http://<VM100_IP>:5000';
$lmStudioBase = 'http://<VM100_IP>:1234/v1';

function http_json_request(string $method, string $url, ?array $payload = null, int $timeout = 15): array {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($method));
    curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);

    $headers = [
        'Accept: application/json'
    ];

    if ($payload !== null) {
        $json = json_encode($payload, JSON_UNESCAPED_UNICODE);
        if ($json === false) {
            throw new RuntimeException('Failed to encode payload to JSON');
        }
        $headers[] = 'Content-Type: application/json';
        $headers[] = 'Content-Length: ' . strlen($json);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $json);
    }

    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $responseBody = curl_exec($ch);
    if ($responseBody === false) {
        $error = curl_error($ch);
        $code = curl_errno($ch);
        curl_close($ch);
        throw new RuntimeException("cURL error ({$code}): {$error}");
    }

    $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    return [$statusCode, $responseBody];
}

function respond(array $payload, int $statusCode = 200): void {
    http_response_code($statusCode);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

try {
    switch ($action) {
        case 'health':
            [$code, $body] = http_json_request('GET', $backendBase . '/health', null, 5);
            http_response_code($code);
            echo $body;
            break;

        case 'metrics':
            [$code, $body] = http_json_request('GET', $backendBase . '/api/shenron/metrics', null, 8);
            http_response_code($code);
            echo $body;
            break;

        case 'lm_health':
            try {
                [$code, $body] = http_json_request('GET', $lmStudioBase . '/models', null, 5);
                $decoded = json_decode($body, true);
                if (!is_array($decoded)) {
                    $decoded = [];
                }

                $models = $decoded['data'] ?? [];
                if (!is_array($models)) {
                    $models = [];
                }

                $success = $code >= 200 && $code < 300;
                respond([
                    'success' => $success,
                    'model_count' => $success ? count($models) : 0,
                    'models' => $success ? $models : [],
                    'message' => $success ? 'LM Studio online' : 'LM Studio responded with an error'
                ], $success ? 200 : 503);
            } catch (RuntimeException $e) {
                respond([
                    'success' => false,
                    'error' => $e->getMessage(),
                    'message' => 'LM Studio unreachable'
                ], 503);
            }
            break;

        case 'start_wish':
            $query = trim($input['query'] ?? '');
            if ($query === '') {
                respond(['error' => "Missing or empty 'query' parameter"], 400);
            }
            $payload = [
                'query' => $query,
                'power_mode' => $input['power_mode'] ?? 'council',
                'use_rag' => $input['use_rag'] ?? true,
                'async_mode' => true,
                'agent_mode' => !empty($input['agent_mode'])
            ];
            [$code, $body] = http_json_request('POST', $backendBase . '/api/shenron/grant-wish', $payload, 10);
            http_response_code($code);
            echo $body;
            break;

        case 'wish_status':
            $jobId = $input['job_id'] ?? '';
            if (!$jobId) {
                respond(['error' => "Missing 'job_id' parameter"], 400);
            }
            [$code, $body] = http_json_request('GET', $backendBase . '/api/shenron/job-status/' . rawurlencode($jobId), null, 8);
            http_response_code($code);
            echo $body;
            break;

        case 'cancel_wish':
            $jobId = $input['job_id'] ?? '';
            if (!$jobId) {
                respond(['error' => "Missing 'job_id' parameter"], 400);
            }
            [$code, $body] = http_json_request('POST', $backendBase . '/api/shenron/cancel-job/' . rawurlencode($jobId), [] , 5);
            http_response_code($code);
            echo $body;
            break;

        case 'fast_mode':
            $modelId = $input['warrior_id'] ?? '';
            $query = trim($input['query'] ?? '');
            if ($modelId === '' || $query === '') {
                respond(['error' => "Missing 'warrior_id' or 'query'"], 400);
            }
            $payload = [
                'model' => $modelId,
                'messages' => [
                    [
                        'role' => 'user',
                        'content' => $query
                    ]
                ],
                'temperature' => $input['temperature'] ?? 0.7,
                'max_tokens' => $input['max_tokens'] ?? 2048
            ];
            [$code, $body] = http_json_request('POST', $lmStudioBase . '/chat/completions', $payload, 60);
            http_response_code($code);
            echo $body;
            break;

        case 'python_heartbeat':
            $started = microtime(true);
            try {
                [$code, $body] = http_json_request('GET', $backendBase . '/health', null, 5);
                $latency = round((microtime(true) - $started) * 1000);
                $decoded = json_decode($body, true);
                if (!is_array($decoded)) {
                    $decoded = [];
                }
                $status = $decoded['status'] ?? null;
                $ok = ($code >= 200 && $code < 300 && $status === 'operational');

                respond([
                    'success' => $ok,
                    'latency_ms' => $latency,
                    'payload' => $decoded,
                    'message' => $ok ? 'Python backend heartbeat OK' : 'Python backend heartbeat failed'
                ], $ok ? 200 : 503);
            } catch (RuntimeException $e) {
                respond([
                    'success' => false,
                    'latency_ms' => null,
                    'error' => $e->getMessage(),
                    'message' => 'Python backend heartbeat failed'
                ], 503);
            }
            break;

        default:
            respond(['error' => 'Unknown action', 'action' => $action], 400);
    }
} catch (RuntimeException $ex) {
    respond([
        'error' => $ex->getMessage()
    ], 500);
}
