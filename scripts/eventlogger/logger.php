TWOX logging :)
<?php

// Change these! 
$servername     = "localhost";
$username       = "user";
$password       = "pass";
$db             = "log";

// This is the command to create the log table
$create = "CREATE TABLE log (
                id int NOT NULL AUTO_INCREMENT,
                event varchar(20), 
                location varchar(20), 
                value varchar(20), 
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (id),  
                INDEX (location), INDEX (event)
            ); ";

// Get the url variables
$event = $_GET['event'];
$location = $_GET['location'];
$limit = array_key_exists('limit', $_GET) ? $_GET['limit'] : 1;
$value = array_key_exists('value', $_GET) ? $_GET['value'] : '';

// If we have the minimum amount of variables, log them
if ($event && $location) {

    // Open a new connection 
    $conn = new mysqli($servername, $username, $password, $db);


    // Check that a certain amount of time has passed since last log instance...
    $do_log = False; 
    $diff_sql = "SELECT TIME_TO_SEC(TIMEDIFF(CURRENT_TIMESTAMP, time)) as diff FROM log WHERE location='$location' AND event='$event' ORDER BY time DESC LIMIT 1";
    $result = $conn->query($diff_sql);
    if ($result->num_rows == 1) { 
        $row = $result->fetch_assoc();
        if ($row['diff'] > $limit ) $do_log = True;        
    } else $do_log = True; 

    // Insert the event into the databse
    if ($do_log) {
        $sql = "INSERT INTO log (location, event, value) VALUES ('$location', '$event', '$value')";
        if ($conn->query($sql) === TRUE) echo "\n\nEvent logged!";
        else echo "\n\nError: " . $sql . "\n" . $conn->error;    
    } else echo "\n\nNot logged :(";
    $conn->close();
}

?>
