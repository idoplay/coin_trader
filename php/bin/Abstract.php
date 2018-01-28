<?php

 class GodAbstract{
    public $querynum = 0;
    public $link;
    public $histories;
    public $time;
    public $tablepre;

    protected $db_config = array();
    public function __construct(){

        /*
        $config = file_get_contents(APP_PATH.'../config.json');
        $this->gconfig = json_decode($config,true);
        $this->mysql_config = $this->gconfig['mysql'];

        $this->connect($this->gconfig['mysql']['stock']['host'], $this->gconfig['mysql']['stock']['user'], $this->gconfig['mysql']['stock']['password'], $this->gconfig['mysql']['stock']['dbname']);
        */$this->logger = $this->logger();
    }

    protected $solomon=null;
    protected function get_solomon(){
        if(is_null($this->solomon)){
            $options = array('CURLOPT_USERAGENT'=> 'Mozilla/5.0 (X11; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1','CURLOPT_REFERER'=>'/');
            $this->solomon  = new solomon($options);
        }
        return $this->solomon;
    }
    public function connect($dbhost, $dbuser, $dbpw, $dbname = '', $dbcharset = 'utf8', $pconnect = 0, $tablepre='', $time = 0) {
        $this->time = $time;
        $this->tablepre = $tablepre;
        if($pconnect) {
            if(!$this->link = mysql_pconnect($dbhost, $dbuser, $dbpw)) {
                $this->halt('Can not connect to MySQL server');
            }
        } else {
            if(!$this->link = mysqli_connect($dbhost, $dbuser, $dbpw, $dbname)) {
                $this->halt('Can not connect to MySQL server');
            }
        }
        if($this->version() > '4.1') {

            if($dbcharset) {
                mysqli_query( $this->link,"SET character_set_connection=".$dbcharset.", character_set_results=".$dbcharset.", character_set_client=binary");
            }

            if($this->version() > '5.0.1') {
                mysqli_query( $this->link,"SET sql_mode=''");
            }
        }

        if($dbname) {
            mysqli_select_db($this->link,$dbname);
        }
        return $this->link;
    }

    public function fetch_array($query, $result_type = MYSQL_ASSOC) {
        return mysqli_fetch_array($query, $result_type);
    }

    public function result_first($sql) {
        $query = $this->query($sql);
        return $this->result($query, 0);
    }

    public function fetch_first($sql) {
        $query = $this->query($sql);
        return $this->fetch_array($query);
    }

    public function fetch_all($sql) {
        $arr = array();
        $query = $this->query($sql);
        while($data = $this->fetch_array($query)) {
            $arr[] = $data;
        }
        return $arr;
    }

    public function cache_gc() {
        $this->query("DELETE FROM {$this->tablepre}sqlcaches WHERE expiry<$this->time");
    }

    public function query($sql, $type = '', $cachetime = FALSE) {
        $func = $type == 'UNBUFFERED' && @function_exists('mysql_unbuffered_query') ? 'mysql_unbuffered_query' : 'mysqli_query';
        if(!($query = $func($this->link,$sql)) && $type != 'SILENT') {
            $this->halt('MySQL Query Error', $sql);
        }
        $this->querynum++;
        $this->histories[] = $sql;
        return $query;
    }
    public function insert($table,$array) {
        if(!is_array($array)) {
            return false;
        }
        $field = $field_v = '';
        foreach($array as $k=>$v) {
            $field .= $k.",";
            $field_v .= "'".$v."',";
        }
        $field = substr($field,0,-1);
        $field_v = substr($field_v,0,-1);
        $this->query("INSERT INTO $table(".$field.") VALUES (".$field_v.")");
        return $this->insert_id();
    }
    public function insert_more($table,$array){
        if(!is_array($array)) {
            return false;
        }
        $field = $field_v = array();
        foreach($array as $k=>$v) {
            //$field .= $k.",";
            $_v = array_values($v);
            $_v = implode("','",$_v);
            $field_v[] = "('".$_v."')";
        }
        $field = implode(',',array_keys($array[0]));

        $this->query("INSERT INTO $table(".$field.") VALUES ".implode(',',$field_v));
    }
    public function update($table,$array,$where) {
        if(!is_array($array)) {
            return false;
        }
        $field = '';
        foreach($array as $k=>$v) {
            $field .= $k."='".$v."',";
        }
        $field = substr($field,0,-1);
        $this->query("UPDATE $table SET $field WHERE $where");
        return $this->affected_rows();
    }

    public function affected_rows() {
        return mysqli_affected_rows($this->link);
    }

    public function error() {
        return (($this->link) ? mysql_error($this->link) : mysql_error());
    }

    public function errno() {
        return intval(($this->link) ? mysql_errno($this->link) : mysql_errno());
    }

    public function result($query, $row) {
        $query = @mysql_result($query, $row);
        return $query;
    }

    public function num_rows($query) {
        $query = mysqli_num_rows($query);
        return $query;
    }

    public function num_fields($query) {
        return mysqli_num_fields($query);
    }

    public function free_result($query) {
        return mysqli_free_result($query);
    }

    public function insert_id() {
        return ($id = mysqli_insert_id($this->link)) >= 0 ? $id : $this->result($this->query("SELECT last_insert_id()"), 0);
    }

    public function fetch_row($query) {
        $query = mysqli_fetch_row($query);
        return $query;
    }

    public function fetch_fields($query) {
        return mysqli_fetch_field($query);
    }

    public function version() {
        return mysqli_get_server_info($this->link);
    }

    public function close() {
        return mysqli_close($this->link);
    }

    public function halt($message = '', $sql = '') {
        exit($message.'<br /><br />'.$sql.'<br /> '.mysql_error());
    }
    protected function logger($fileName=''){
        if(!$fileName){
            $fileName = APP_PATH . '/logs/'.date('Y-m-d').'.log';
        }
        while (true) {
            file_put_contents($fileName, yield . "\n", FILE_APPEND);
        }
    }

    public function debug($str = '') {echo "\n".PHP_EOL . date('Y-m-d H:i:s') . ": " . $str . PHP_EOL;}

    public function __destruct() {
        $this->close();
        unset($this->link);
        unset($this->solomon);
/*
        $start_time = date("Y-m-d H:i:s", JOB_START_TIME);
        $end_microtime = microtime(true);
        $end_time = date('Y-m-d H:i:s');
        $cost_time = sprintf("%f", $end_microtime - JOB_START_TIME);

        $out_put = "\n开始时间:{$start_time},\n";
        $out_put .= "结束时间:{$end_time},\n";
        $out_put .= "总耗时:{$cost_time}s,\n";
        echo $out_put;*/
    }
    public function input($str){
        $res = '';
        if(!empty($_GET[$str])){
            $res = $_GET[$str];
        }elseif(!empty($_POST[$str])){
            $res = $_POST[$str];
        }
        return $res;
    }
    protected function json_success($msg,$data=array(),$code=200){
        $res = array(
            'count'=>count($data),
            'status'=>1,
            'code'=>$code,
            'message'=>$msg,
            'result'=>$data
            );
        $debug = $this->input('_debug',0);
        if($debug ==1){
            echo $this->jsonFormat($res);
        }
        header('Content-Type: application/json');
        echo json_encode($res);exit;
    }
    //统计数据返回 用于标识返回的结果是成功1或失败0
    protected function json_error($msg,$data=array(),$code=200){
        $res = array(
            'count'=>count($data),
            'status'=>0,
            'code'=>$code,
            'message'=>$msg,
            'result'=>$data
            );
        $debug = $this->input('_debug',0);
        if($debug ==1){
            echo $this->jsonFormat($res);
        }
        header('Content-Type: application/json');
        echo json_encode($res);exit;
    }
    //格式化json串,用来写文档中
    public function jsonFormat($data, $indent=null){
        // 对数组中每个元素递归进行urlencode操作，保护中文字符
        array_walk_recursive($data, 'self::jsonFormatProtect');
        $data = json_encode($data);
        // 将urlencode的内容进行urldecode
        $data = urldecode($data);
        // 缩进处理
        $ret = '';
        $pos = 0;
        $length = strlen($data);
        $indent = isset($indent)? $indent : '    ';
        $newline = "\n";
        $prevchar = '';
        $outofquotes = true;

        for($i=0; $i<=$length; $i++){
            $char = substr($data, $i, 1);
            if($char=='"' && $prevchar!='\\'){
                $outofquotes = !$outofquotes;
            }elseif(($char=='}' || $char==']') && $outofquotes){
                $ret .= $newline;
                $pos --;
                for($j=0; $j<$pos; $j++){
                    $ret .= $indent;
                }
            }
            $ret .= $char;
            if(($char==',' || $char=='{' || $char=='[') && $outofquotes){
                $ret .= $newline;
                if($char=='{' || $char=='['){
                    $pos ++;
                }
                for($j=0; $j<$pos; $j++){
                    $ret .= $indent;
                }
            }
            $prevchar = $char;
        }
        return $ret;
    }




    /** 将数组元素进行urlencode
    * @param String $val
    */
    static function jsonFormatProtect(&$val){
        if($val!==true && $val!==false && $val!==null && !is_object($val)){
            $val = urlencode($val);
        }
    }


        //字符串的字符集，包括有 utf-8|gb2312|gbk|big5 编码
    public static function spStrlen($str, $charset="utf-8"){
        $re['utf-8']    = "/[\x01-\x7f]|[\xc2-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf]{2}|[\xf0-\xff][\x80-\xbf]{3}/";
        $re['gb2312']   = "/[\x01-\x7f]|[\xb0-\xf7][\xa0-\xfe]/";
        $re['gbk']      = "/[\x01-\x7f]|[\x81-\xfe][\x40-\xfe]/";
        $re['big5']     = "/[\x01-\x7f]|[\x81-\xfe]([\x40-\x7e]|\xa1-\xfe])/";
        preg_match_all($re[$charset], $str, $match);
        return count($match[0]);
    }
}