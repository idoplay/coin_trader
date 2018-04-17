<?php
$url = isset($_GET['u']) ? $_GET['u'] :'';
$res = array(
    'status'=>0,
    'msg'=>'error',
    'result'=>array()
);
if(empty($url)){
    echo json_encode($res);exit;
}
$url = base64_decode($url);
$c = file_get_contents($url);
echo $c;exit;
$d = json_decode($c,true);

if(!isset($d['code'])){
    $res = array(
        'status'=>1,
        'msg'=>'ok',
        'result'=>$d['result']
    );
}elseif(isset($d['code']) && $d['code']==1000){
    $res = array(
        'status'=>1,
        'msg'=>'ok',
        'result'=>$d['message']['datas']
    );
}else{
    $res['msg'] = $d['message'];
}
echo json_encode($res);exit;