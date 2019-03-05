<?php
    $user = getenv('MYSQL_USER') ?: 'root';
    $password = getenv('MYSQL_PASSWORD') ?: 'root';
    $dsn = getenv("MYSQL_DSN") ?: "mysql:host=127.0.0.1;port=3306;dbname=transactions";

    // $mysqli = new mysqli("127.0.0.1", "root", "", "transactions", null, "/cloudsql/storage-options-228714:us-central1:sql-transactions"); 
    // $mysqli = mysqli_connect(null, "root", "", "transactions", null, "/cloudsql/storage-options-228714:us-central1:sql-transactions"); 

    /*
    $cloud_sql_instance_name = getenv("CLOUD_SQL_INSTANCE_NAME");
    $dbname = getenv("MYSQL_DATABASE");*/

    $db = new PDO($dsn, $user, $password);
    
    if (!$db) {
      die("Connection failed: " . mysqli_connect_error());
    }

    // $db = new PDO('mysql:dbname=transactions;unix_socket=/cloudsql/storage-options-228714:us-central1:sql-transactions', 'root');
    // $db = new PDO("mysql:host=127.0.0.1;dbname=transactions;unix_socket=/cloudsql/storage-options-228714:us-central1:sql-transactions", 'root', 'root');
    // $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("SELECT * from entries");
    $statement->execute();

    // $result = $mysqli->query("SELECT * FROM entries");
    // $sql = "SELECT * FROM entries";
    // $result = mysqli_query($mysqli, $sql);
    
    /*
    while($row = mysqli_fetch_assoc($result)) {
      echo " - " . $row["id"] . ' ';
    }
    */
        
    $all = $statement->fetchAll();

    foreach ($all as $data) {
      echo $data["id"];
    }
    
?>