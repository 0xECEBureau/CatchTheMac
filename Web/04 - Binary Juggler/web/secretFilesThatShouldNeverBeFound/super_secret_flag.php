<?php
session_start();
if (!isset($_SESSION["user_id"])) {
    die("Unauthorized access!");
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flag</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
        }

        .container {
            max-width: 900px; /* wider for long flags */
            margin-top: 100px;
        }

        .card {
            background-color: #1e1e1e;
            border-radius: 10px;
            word-break: break-word;
        }

        .flag {
            font-size: 1.5rem;
            font-weight: bold;
            color: #ff3860;
            font-family: monospace;
            overflow-wrap: break-word;
        }
    </style>
</head>
<body>
    <div class="container text-center">
        <div class="card p-4 shadow-lg w-100">
            <h2>Welcome to the Challenge!</h2>
            <p class="flag"><?= htmlspecialchars("MAC{Typ3_jugg11ng_1s_s0_stup1d_h00rah_php}"); ?></p>
        </div>
    </div>
</body>
</html>
