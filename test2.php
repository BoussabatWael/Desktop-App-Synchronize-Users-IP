<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Credentials: true");
header("Access-Control-Max-Age: 100");
header("Access-Control-Allow-Headers: X-Requested-With, Content-Type, Origin, Cache-Control, Pragma, Authorization, Accept, Accept-Encoding");
header("Access-Control-Allow-Methods: PUT, POST, GET, OPTIONS, DELETE");
header('Content-Type: application/json; charset=utf-8');

$_POST = json_decode(file_get_contents('php://input'), true);

$server_id = $_POST["server_id"];
$Task = $_POST["Task"];
chdir('C:\Users\waelb\AppData\Local\Programs\Python\Python310');
if ($Task == "Connect") {
	$username = $_POST["username"];
    $password = $_POST["password"];
	$port = $_POST["port"];
    $response = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$username.'" "'.$password.'" "'.$port.'"');
    echo $response;
}
if ($Task == "from_desktop") {
	$ip_address = $_POST["ip_address"];
    $port = $_POST["port"];
	$protocol = $_POST["protocol"];
	$action = $_POST["action"];
    $response = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$ip_address.'" "'.$port.'" "'.$protocol.'" "'.$action.'"');
    echo $response;
}
if ($Task == "deny") {
	$rule_id = $_POST["rule_id"];
    $response = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$rule_id.'"');
    echo $response;
	
}
if ($Task == "check_os") {
    $response = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $response;
}
if ($Task == "add") {
    $ip_address = $_POST["ip_address"];
	$protocol = $_POST["protocol"];
	$port = $_POST["port"];
    $action = $_POST["action"];
    $response = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$ip_address.'" "'.$protocol.'" "'.$port.'" "'.$action.'"');
    echo $response;
}
if ($Task == "edit") {
    $ruleId = $_POST["ruleId"];
	$new_protocol = $_POST["new_protocol"];
    $new_ip_address = $_POST["new_ip_address"];
	$new_port = $_POST["new_port"];
    $new_action = $_POST["new_action"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$ruleId.'" "'.$new_protocol.'" "'.$new_ip_address.'" "'.$new_port.'" "'.$new_action.'"');
    echo $result;
}
if ($Task == "delete") {
    $id_rule = $_POST["id_rule"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$id_rule.'"');
    echo $result;
}

if ($Task == "list") {
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $result;
}
if ($Task == "check") {
    $r_ip_address = $_POST["r_ip_address"];
    $r_action = $_POST["r_action"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$r_ip_address.'" "'.$r_action.'"');
    echo $result;
}
if ($Task == "accesslogs") {
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $result;
}
if ($Task == "securelogs") {
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $result;
}
if ($Task == "csf") {
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $result;
}

if ($Task == "openedports") {
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $result;
}
if ($Task == "services") {
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $result;
}
if ($Task == "startservice") {
    $service = $_POST["service"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$service.'"');
    echo $result;
}
if ($Task == "restartservice") {
    $service = $_POST["service"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$service.'"');
    echo $result;
}
if ($Task == "stopservice") {
    $service = $_POST["service"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$service.'"');
    echo $result;
}
if ($Task == "checkport") {
    $host = $_POST["host"];
    $port = $_POST["port"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$host.'" "'.$port.'"');
    echo $result;
}
if ($Task == "checkip") {
    $host = $_POST["host"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$host.'"');
    echo $result;
}
if ($Task == "installservice") {
    $service = $_POST["service"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$service.'"');
    echo $result;
}
if ($Task == "fail2banlogs") {
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $result;
}
if ($Task == "fail2banIPbanned") {
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'"');
    echo $result;
}
if ($Task == "addurl") {
    $url_to_protect = $_POST["url_to_protect"];
    $ip_add = $_POST["ip_add"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$url_to_protect.'" "'.$ip_add.'"');
    echo $result;
}
if ($Task == "updateurl") {
    $id_url = $_POST["id_url"];
    $url2 = $_POST["url2"];
    $ip_address2 = $_POST["ip_address2"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$id_url.'" "'.$url2.'" "'.$ip_address2.'"');
    echo $result;
}
if ($Task == "deleteurl") {
    $url = $_POST["url"];
    $result = exec('python C:/Users/waelb/AppData/Local/Programs/Python/Python310/firewall.py "'.$server_id.'" "'.$Task.'" "'.$url.'"');
    echo $result;
}

?>