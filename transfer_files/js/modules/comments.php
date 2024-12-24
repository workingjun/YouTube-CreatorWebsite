<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

header("Content-Type: application/json"); // JSON 형식으로 응답
header("Access-Control-Allow-Origin: *"); // 모든 도메인에서 접근 허용

// MySQL 데이터베이스 연결 설정
$servername = "218.151.69.98";
$username = "youtube"; // 데이터베이스 사용자
$password = "2483"; // 데이터베이스 비밀번호
$database = "youtubeDATA"; // 데이터베이스 이름

// 데이터베이스 연결
$conn = new mysqli($servername, $username, $password, $database);

// 연결 확인
if ($conn->connect_error) {
    echo json_encode(['error' => 'Database connection failed: ' . $conn->connect_error]);
    exit();
}

// videoId 가져오기
if (isset($_GET['videoId'])) {
    $videoId = $conn->real_escape_string($_GET['videoId']);

    // 댓글 데이터 가져오기 쿼리
    $sql = "SELECT author, text, like_count, created_at FROM comments WHERE video_id = '$videoId'";
    $result = $conn->query($sql);

    $comments = [];
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $comments[] = $row; // 각 행을 배열에 추가
        }
    }

    echo json_encode($comments); // JSON 형식으로 댓글 데이터 반환
} else {
    echo json_encode(['error' => 'videoId is missing']);
}

$conn->close(); // 데이터베이스 연결 종료
?>

