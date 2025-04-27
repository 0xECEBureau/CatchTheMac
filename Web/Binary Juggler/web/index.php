<?php
session_start();

// Check if there's an error message in the session and display it
if (isset($_SESSION["login_error"])) {
    echo "<p style='color: red;'>" . $_SESSION["login_error"] . "</p>";
    unset($_SESSION["login_error"]); // Clear the error after displaying it
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    // Type juggling vulnerability
    if (md5($password) == "0e123123464646876543456789") {
        $_SESSION["user_id"] = 1; // Hardcode a user_id for session validation
        header("Location: secretFilesThatShouldNeverBeFound/super_secret_flag.php");
        exit();
    } else {
        $_SESSION["login_error"] = "Invalid login!";
        header("Location: index.php");
        exit();
    }
}
?>

<!-- Fake anonymous hacker commentary -->
<div style="font-size: 12px; color: #f0f0f0; background-color: #1e1e1e; padding: 10px; margin-top: 20px; font-family: 'Courier New', monospace;">
    <p><strong>[Binary juggler]</strong></p>
    <p><i>Salut, juste un petit tuyau en passant… J’ai découvert qu’ils utilisent du <strong>hash MD5</strong> pour stocker les mots de passe.</i></p>
    <p><strong>À retenir :</strong> Les mots de passe sont censés être difficiles à deviner… mais je pense pas qu’on ait besoin de le deviner.</p>
    <p><i>"Where in the world is the admin password..."</i></p>
</div>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CTF Challenge</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #121212; /* Dark mode */
            color: #ffffff;
        }
        .container {
            max-width: 400px;
            margin-top: 100px;
        }
        .card {
            background-color: #1e1e1e;
            border-radius: 10px;
        }
        .btn-primary {
            background-color: #ff3860;
            border-color: #ff3860;
        }
        .btn-primary:hover {
            background-color: #ff1744;
            border-color: #ff1744;
        }
    </style>
</head>
<body>
    <div class="container text-center">
        <div class="card p-4 shadow-lg">
            <h2>Login</h2>
            <form action="index.php" method="POST">
                <div class="mb-3">
                    <input type="text" name="username" class="form-control" placeholder="Username" required>
                </div>
                <div class="mb-3">
                    <input type="password" name="password" class="form-control" placeholder="Password" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
        </div>
    </div>
</body>
</html>
