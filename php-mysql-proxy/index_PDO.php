<?php
    $user = getenv('MYSQL_USER');
    $password = getenv('MYSQL_PASSWORD');
    $dsn = getenv("MYSQL_DSN") ?: "mysql:host=127.0.0.1;port=3306;dbname=[MYSQL_DB_NAME]";

    $db = new PDO($dsn, $user, $password);

    try {
        $db = new PDO($dsn, $user, $password);

        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        echo "Connected successfully"; 
        }
    catch(PDOException $e)
        {
        echo "Connection failed: " . $e->getMessage();
        }

    $statement = $db->prepare("SELECT * from [MYSQL_TABLE_NAME]");
    $statement->execute();
    $all = $statement->fetchAll();

    foreach ($all as $data) {
      echo $data["id"];
    }
?>