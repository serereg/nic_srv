
<?php
if(isset($_GET['val'])) 
{
	$fd = fopen("data.txt", 'w') or die("�� ������� ������� ����");
	$str = $_GET['val'];
	fwrite($fd, $str);
	fclose($fd);
}
else
{
	$str = htmlentities(file_get_contents("data.txt"));
	echo $str;
}
?>