<?php

    /*
    **     Very simple interface script for triggering events on remote devices
    **
    **     Usage: http://thedevice/event/?name=play-sound&value=doorbell
    */

    $eventdir  = '/home/pi/events/';   // This directory needs the correct permission
    $name      = array_key_exists('name', $_GET) ? $_GET['name'] : '';
    $value     = array_key_exists('value', $_GET) ? $_GET['value'] : '0';
 
    if ($name) $ret = file_put_contents($eventdir . $name, $value);

?>

