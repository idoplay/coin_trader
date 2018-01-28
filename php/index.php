<?php


$base_uri = DIRECTORY_SEPARATOR=='/' ? dirname($_SERVER["SCRIPT_NAME"]) : str_replace('\\', '/', dirname($_SERVER["SCRIPT_NAME"]));
define("BASE_URI", $base_uri =='/' ? '' : $base_uri);
unset($base_uri);
define('APP_NAME', 'mv-jobs');
define('APP_PATH', realpath(dirname(__FILE__)).'/');
define('JOB_START_TIME', microtime(true));


function  echo_msg($str){
    echo $str."\r\n";exit;
}
function displayHelp()
{
    echo <<<EOF
Composer Installer
------------------
Options
--help               this help
--check              for checking environment only
--force              forces the installation
--ansi               force ANSI color output
--no-ansi            disable ANSI color output
--quiet              do not output unimportant messages
--install-dir="..."  accepts a target installation directory
--version="..."      accepts a specific version to install instead of the latest
--filename="..."     accepts a target filename (default: composer.phar)
--disable-tls        disable SSL/TLS security for file downloads
--cafile="..."       accepts a path to a Certificate Authority (CA) certificate file for SSL/TLS verification

EOF;
}
$help = in_array('--help', $argv);
if($help){
    displayHelp();
    exit(0);
}



if(count($argv) < 2){
    echo_msg("Param Error");
}


$_bin_path = array('bin');
if (strpos($argv[1],'_')===false) {
    $class = $argv[1];

}else{
    list($path,$class) = explode('_',$argv[1]);
    $_bin_path[] = $path;
}
$_bin_path[]= $class;

$config_json = json_decode(file_get_contents(APP_PATH."../config.json"),true);
$file = APP_PATH . implode('/',$_bin_path).".php";
echo $file;
if(!file_exists($file)){
    echo_msg('Class '.$argv[1]." Not Found");
}
require ($file);
unset($argv[0]);
unset($argv[1]);

$param = $argv;
$bll = new $class();
$bll->set_config($config_json);
$bll->run($param);
