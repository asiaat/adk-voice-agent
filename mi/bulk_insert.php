<?php
// --- Configuration ---
// Set error reporting for development. In production, you should log errors instead of displaying them.
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Set the content type of the response to JSON
header("Content-Type: application/json");

// Define your secret API key
define('API_KEY', 'Zala2025Yane!'); 

// Database credentials
$host = "127.0.0.1"; // Or your actual Hostinger MySQL host
$user = "u114264882_hyberw";
$pass = "Qyber2025S6da!";
$db = "u114264882_hyberw";

// --- Security Check ---
// Verify the API key from the request headers
$headers = getallheaders();
if (!isset($headers['x-api-key']) || $headers['x-api-key'] !== API_KEY) {
    http_response_code(401); // Unauthorized
    echo json_encode(["status" => "error", "message" => "Unauthorized: Invalid or missing API key."]);
    exit;
}

// --- Database Connection ---
// Establish a connection to the database using MySQLi
$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    http_response_code(500); // Internal Server Error
    echo json_encode(["status" => "error", "message" => "Database connection failed: " . $conn->connect_error]);
    exit;
}
// Set charset to utf8mb4 to support a wide range of characters
$conn->set_charset("utf8mb4");

// --- Input Processing ---
// Read the raw POST data from the request
$raw_input = file_get_contents("php://input");
$data = json_decode($raw_input, true);

// Validate the incoming JSON
if (json_last_error() !== JSON_ERROR_NONE || !is_array($data)) {
    http_response_code(400); // Bad Request
    echo json_encode(["status" => "error", "message" => "Invalid JSON provided."]);
    exit;
}

// --- Data Extraction ---
// Flatten the nested structure to get a simple list of articles
$articles = [];
foreach ($data as $entry) {
    if (isset($entry['articles']['results']) && is_array($entry['articles']['results'])) {
        // array_merge is efficient for combining arrays
        $articles = array_merge($articles, $entry['articles']['results']);
    }
}

if (empty($articles)) {
    http_response_code(400); // Bad Request
    echo json_encode(["status" => "error", "message" => "No articles found in the provided data."]);
    exit;
}

// --- Bulk Insert Preparation ---
// This is the efficient way to insert multiple rows.
// ON DUPLICATE KEY UPDATE prevents errors if you try to insert an article with an existing `id`
// and instead updates the specified fields.
$query = "
    INSERT INTO data_table (id, head, url, locations, authors, datetime, summary, vectors) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON DUPLICATE KEY UPDATE 
        head = VALUES(head), 
        url = VALUES(url), 
        authors = VALUES(authors), 
        datetime = VALUES(datetime), 
        summary = VALUES(summary);
";

$stmt = $conn->prepare($query);
if (!$stmt) {
    http_response_code(500); // Internal Server Error
    echo json_encode(["status" => "error", "message" => "Failed to prepare statement: " . $conn->error]);
    exit;
}

$inserted_count = 0;
$skipped_count = 0;

// Begin a transaction for atomicity. All inserts will succeed, or none will.
$conn->begin_transaction();

try {
    foreach ($articles as $article) {
        // --- Data Mapping and Cleaning ---
        $id        = $article['uri'] ?? null;
        $head      = $article['title'] ?? null;
        $url       = $article['url'] ?? null;
        $datetime  = $article['dateTimePub'] ?? null;
        $summary   = $article['body'] ?? null;

        // Skip rows with essential missing data
        if (is_null($id) || is_null($head) || is_null($url) || is_null($datetime) || is_null($summary)) {
            $skipped_count++;
            continue;
        }

        // Default or derived values
        $locations = 'any'; // Default value
        $vectors   = 'test'; // Placeholder for future NLP processing
        
        // Safely implode authors array into a string
        $authors_array = array_map(fn($auth) => $auth['name'] ?? null, $article['authors'] ?? []);
        $authors = implode(", ", array_filter($authors_array)); // array_filter removes nulls

        // Bind parameters and execute for each article
        // The types string 'isssssss' corresponds to:
        // i: integer (id), s: string, s: string, s: string, s: string, s: string, s: string, s: string
        $stmt->bind_param("isssssss", $id, $head, $url, $locations, $authors, $datetime, $summary, $vectors);
        
        if ($stmt->execute()) {
            $inserted_count++;
        }
    }

    // If all executions were successful, commit the transaction
    $conn->commit();

    http_response_code(201); // Created
    echo json_encode([
        "status" => "success",
        "message" => "Bulk operation completed.",
        "processed" => $inserted_count,
        "skipped" => $skipped_count
    ]);

} catch (mysqli_sql_exception $e) {
    // If any execution fails, roll back the entire transaction
    $conn->rollback();
    http_response_code(500); // Internal Server Error
    echo json_encode(["status" => "error", "message" => "A database error occurred during insertion.", "details" => $e->getMessage()]);
} finally {
    // --- Cleanup ---
    $stmt->close();
    $conn->close();
}

