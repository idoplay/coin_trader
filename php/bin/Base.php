<?php
require_once('Abstract.php');

class Base extends GodAbstract {

    public function run($param){
        $func = $param[2];

        /*$this->_post_code = empty($param[3]) ? '': $param[3];
        $this->redis = new redis();
        $this->redis->connect('127.0.0.1', 6379);*/
        $this->$func($param);
    }

    public function set_config($config){
        $this->db_config = $config['mysql'];
    }
    private function _init_words_db(){
        $config = $this->db_config['words'];
        $this->db_words = connect($config['host'],$config['user'],$config['password'], 'words');
    }

    public function shortUrl($url){
        $base32 = array (
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
            'y', 'z', '0', '1', '2', '3', '4', '5','6','7','8','9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        );

        $hex = md5($url);
        $hexLength = strlen($hex);
        $subHexLen = $hexLength / 8;

        $output = array();
        for ($i = 0; $i < $subHexLen; $i++) {
            //每循环一次取到8位
            $subHex = substr ($hex, $i * 8, 8);
            $int = 0x3FFFFFFF & (1 * ('0x'.$subHex));
            $out = '';

            for ($j = 0; $j < 6; $j++) {
                $val = 0x0000001F & $int;
                $out .= $base32[$val];
                $int = $int >> 5;
            }

            $output[] = $out;
        }

        return $output;
    }
    private function demo(){
        print "Php demo";
        $url =1;
        $this->debug("String length:1======\n".$url);
        /*
        $db = new db();
        $config = $this->mysql_config['quncms'];
        $db->connect($config['host'],$config['user'],$config['password'], $config['dbname']);
        */
        /*
        $_cn = $this->fetch_all("select id from s_stock_trade where s_code='".$value['s_code']."'");
        $count = count($_cn);
        $url = $this->get_solomon()->get("http://data.gtimg.cn/flashdata/hushen/latest/daily/".$value['s_code'].".js");
        #http://data.gtimg.cn/flashdata/hushen/latest/daily/sz000982.js
        $_rs = $this->get_solomon()->spMatch('total:','start',$url);
        */

        /*


        */
    }

    public function save_baidu_words($param=array()){
        $param2 = base64_decode($param[3]);
        $param2 = json_decode($param2);
        if(empty($param2)){
            return false;
        }
        foreach ($param2 as $value) {
            $hash = $this->shortUrl($value);
            $has = $this->redis->get($hash[0]);

            if(empty($has)){
                $in = array(
                    'word'=>$value,
                    'hash_str'=>$hash[0],
                    'dateline'=>date('Ymd')
                    );
                $this->db->insert('word_list',$in);
                $this->redis->set($hash[0],1);
            }
            $hash2 = $hash[0].'-'.date('Ymd');
            $has2 = $this->redis->get($hash2);
            if(empty($has2)){
                $in = array(
                    'word'=>$value,
                    'dateline'=>date('Ymd')
                    );
                $this->db->insert('daily_word',$in);
                $this->redis->set($hash2,1);
            }
            /*
            $has = $db->fetch_first("select * from word_list where hash_str='".$hash[0]."'");
            if(empty($has)){
                $in = array(
                    'word'=>$value,
                    'hash_str'=>$hash[0],
                    'dateline'=>date('Ymd')
                    );
                $db->insert('word_list',$in);
                $in = array(
                    'word'=>$value,
                    'dateline'=>date('Ymd')
                    );
                $db->insert('daily_word',$in);
            }*/
        }
    }
}