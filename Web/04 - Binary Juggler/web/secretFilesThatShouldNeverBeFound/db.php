<?php
$mysqli = new mysqli("db", "ctfuser", "ctfpassword", "ctf_db");

if ($mysqli->connect_error) {
    die("Database connection failed: " . $mysqli->connect_error);
}
?>