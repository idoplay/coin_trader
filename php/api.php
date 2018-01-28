<?php
define('APP_PATH', realpath(dirname(__FILE__)).'/');
require_once('bin/Api.php');

$api = new Api();
$config_json = json_decode(file_get_contents(APP_PATH."../config.json"),true);
$api->set_config($config_json);

$c = isset($_GET['c']) ? $_GET['c'] : '';
if(empty($c)){
    echo "not found function";
    exit(1);
}

$api->$c();