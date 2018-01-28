<?php
require_once('Abstract.php');

class Api extends GodAbstract {

    private $db_words = null;
    public function __construct(){
        parent::__construct();
    }
    public function set_config($config){
        $this->db_config = $config['mysql'];
    }
    private function _init_words_db(){
        //$this->db_words = new db();
        $config = $this->db_config['words'];
        $this->db_words = $this->connect($config['host'],$config['user'],$config['password'], 'words');
    }
    private function _log($str){
        $debug = "====".date('Y-m-d H:i:s')."======\n";
        $debug .= var_export($str,true)."\n";
        file_put_contents('/tmp/soga_api.log', $debug,FILE_APPEND);
    }
    public function baseWords(){
        $this->_init_words_db();
        #获取基础词
        $all = $this->fetch_all("select * from base where 1");
        $res = array();
        foreach ($all as $value) {
            $res[] = $value['name'];
        }
        $this->json_success('done',$res);
    }
    public function twoWords(){
        #4个字以内
        $this->_init_words_db();
        $all = $this->fetch_all("select * from good_keywords where 1 ");
        $res = array();
        foreach ($all as $value) {
            if(ctype_alnum($value['words'])){
                $res[] = $value['words'];
            }else{
                if($this->spStrlen($value['words']) < 5){
                    $res[] = $value['words'];
                }
            }
        }
        $this->json_success('done',$res);
    }

    public function run(){
        $this->_init_words_db();

        $str = file_get_contents("php://input");
        $str = json_decode($str,true);
        $this->_log($str);
        if(empty($str)){
            $this->json_error('str length');
        }
        foreach ($str as $value) {
            $in = array(
                'hash_str'=>$value[2],
                'words'=>$value[0],
                'channel'=>'tb',
                'dateline'=>date('Ymd'),
                'c_num'=>intval($value[1])
                );

            $has = $this->fetch_first("select * from good_keywords where hash_str='".$value[2]."'");
            if(empty($has)){
                $this->insert('good_keywords',$in);
            }else{
                $this->update('good_keywords',array('dateline'=>date('Ymd'),'c_num'=>intval($value[1])),array('id'=>$has['id']));
            }
        }
        $this->json_success('done');

    }
}