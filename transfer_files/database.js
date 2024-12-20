const express = require('express');
const mysql = require('mysql2');
const app = express();
const port = 3306;

// MySQL 데이터베이스 연결 설정
const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

// 댓글 데이터 조회 API
app.get('/comments/:videoId', (req, res) => {
  const videoId = req.params.videoId;

  const query = 'SELECT author, text, like_count FROM comments WHERE video_id = ?';
  db.query(query, [videoId], (err, results) => {
    if (err) {
      console.error('Error fetching comments:', err);
      return res.status(500).json({ error: 'Error fetching comments' });
    }

    res.json(results);
  });
});

// 서버 시작
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
