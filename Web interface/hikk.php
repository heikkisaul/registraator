<?php


function tocsv($comm,$da){
	$host="localhost";
	$port=3306;
	$socket="";
	$user="lrb_web";
	$password="zmRpRb4qmbTL0Ke7";
	$dbname="lect_reg_base";
	$data="";
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
		or die ('Could not connect to the database server' . mysqli_connect_error());
	$export = mysqli_query($con, $comm) or die("Query fail: " . mysqli_error());
	$finfo = mysqli_fetch_fields($export);
	if ($comm=="CALL `lect_reg_base`.`GET_LECTURE_ATTENDEES`(".$da.")"){
		foreach ($finfo as $val) {
			switch ($val->name) {

				case LAST_NAME:
					$data .= '"Perekonnanimi",';
					break;
				case FIRST_NAME:
					$data .= '"Eesnimi",';
					break;
				case ID_CODE:
					$data .= '"Isikukood",';
					break;
			}
        }
		$data .="\n";
		while ($row = mysqli_fetch_array($export)){   
		$data .='"'.$row[0].'","'.$row[1].'","'.$row[2].'"'."\n"; 
		}
	}
	else{
		foreach ($finfo as $val) {
			switch ($val->name) {
				case SUBJECT_NAME:
					$data .= '"Aine nimi",';
					break;
				case LECTURE_ID:
					$data .= '"Loengu ID",';
					break;
				case LECTURE_INFO:
					$data .= '"Loengu info",';
					break;
				case LECTURE_START_TIME:
					$data .= '"Loengu algusaeg",';
					break;
				case LECTURE_END_TIME:
					$data .= '"Loengu lõpuaeg",';
					break;
				case LAST_NAME:
					$data .= '"Perekonnanimi",';
					break;
				case FIRST_NAME:
					$data .= '"Eesnimi",';
					break;
				case ID_CODE:
					$data .= '"Isikukood",';
					break;
				case SUBJECT_CODE:
					$data .= '"Ainekood",';
					break;
			}
		}
		$data .="\n";
		while($rows=mysqli_fetch_assoc($export)){  
			foreach ($rows as $row){	
				$value.= '"'.$row .'"'.",";
			}
			$data.= $value."\n";
			$value='';
		}	
	}
	$data = str_replace( "\r" , "" , $data );
	if ( $data == "" )
	{
		$data = "\n(0) Records Found!\n";                        
	}
	header("Content-type: application/octet-stream");
	$date = date_create();
	header("Content-Disposition: attachment; filename=reg_andmed_".$date->format('Y-m-d_H:i:s').".csv");
	header("Pragma: no-cache");
	header("Expires: 0");
	print "$data";
}

function attendees($id){
	$host="localhost";
	$port=3306;
	$socket="";
	$user="lrb_web";
	$password="zmRpRb4qmbTL0Ke7";
	$dbname="lect_reg_base";
	$data="";
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
		or die ('Could not connect to the database server' . mysqli_connect_error());
	$result = mysqli_query($con, "CALL `lect_reg_base`.`GET_LECTURE_ATTENDEES`(".$id.")") or die("Query fail: " . mysqli_error());

	$row = mysqli_fetch_array($result);
	echo "<h3>".$row[3]." : ".$row[4]."</h3><br/>";
	$finfo = mysqli_fetch_fields($result);
	foreach ($finfo as $val) {
		switch ($val->name) {

			
			case LAST_NAME:
				$data .= '<table class="table table-bordered"> <tr><th>Perekonnanimi</th>';
				break;
			case FIRST_NAME:
				$data .= '<th>Eesnimi</th>';
				break;
			case ID_CODE:
				$data .= '<th>Isikukood</th></tr>';
				break;
			
		}
        }	
	echo $data;
	echo '<tr><td>'.$row[0] .'</td><td>'. $row[1].'</td><td>'. $row[2].'</td></tr>'; 
	while ($row = mysqli_fetch_array($result)){   
	echo '<tr><td>'.$row[0] .'</td><td>'. $row[1].'</td><td>'. $row[2].'</td></tr>';	
	
	}
	echo '</table>';
}
function subject_lect($id){
	$host="localhost";
	$port=3306;
	$socket="";
	$user="lrb_web";
	$password="zmRpRb4qmbTL0Ke7";
	$dbname="lect_reg_base";
	$data="";
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
		or die ('Could not connect to the database server' . mysqli_connect_error());
	$result = mysqli_query($con, 'CALL `lect_reg_base`.`GET_SUBJECT_LECTURES`("'.$id.'")') or die("Query fail: " . mysqli_error());
	$finfo = mysqli_fetch_fields($result);
	foreach ($finfo as $val) {
		switch ($val->name) {

			case SUBJECT_NAME:
				$data .= '<table class="table table-bordered"> <tr><th>Aine nimi</th>';
				break;
			case LECTURE_ID:
				$data .= '<th>Loengu ID</th>';
				break;
			case LECTURE_INFO:
				$data .= '<th>Loengu info</th>';
				break;
			case LECTURE_START_TIME:
				$data .= '<th>Loengu algusaeg</th>';
				break;
			case LECTURE_END_TIME:
				$data .= '<th>Loengu l'.chr(244).'puaeg</th>';
				break;
			case LAST_NAME:
				$data .= '<th>'.chr(244).'ppej'.chr(244).'ud</th></tr>';
				break;

		}
        }
	echo $data;
	while ($row = mysqli_fetch_array($result)){   
		echo '<tr><td>'.$row[0].'</td><td>'.$row[1].'</td><td>'.$row[2].'</td><td>'.$row[3].'</td><td>'.$row[4].'</td><td>'.$row[5].'</td></tr>'; 
	}
	echo '</table>';
}
function attendance($id){
	$host="localhost";
	$port=3306;
	$socket="";
	$user="lrb_web";
	$password="zmRpRb4qmbTL0Ke7";
	$dbname="lect_reg_base";
	$data="";
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
		or die ('Could not connect to the database server' . mysqli_connect_error());
	$result = mysqli_query($con, "CALL `lect_reg_base`.`GET_USER_ATTENDANCE`(".$id.")") or die("Query fail: " . mysqli_error());
	$finfo = mysqli_fetch_fields($result);
	foreach ($finfo as $val) {
		switch ($val->name) {

			case SUBJECT_NAME:
				$data .= '<table class="table table-bordered"> <tr><th>Aine nimi</th>';
				break;
			case SUBJECT_CODE:
				$data .='<th>Ainekood</th>';
				break;
			case LECTURE_START_TIME:
				$data .= '<th>Loengu algusaeg</th>';
				break;
			case LECTURE_END_TIME:
				$data .='<th>Loengu l'.chr(244).'puaeg</th></tr>';
				break;			
		}		
    }
	echo $data;
	 while ($row = mysqli_fetch_array($result)){   
		echo '<tr><td>'.$row[0].'</td><td>'.$row[1].'</td><td>'.$row[2].'</td><td>'.$row[3].'</td></tr>';
	}
	echo '</table>';
}

function lecturer($id){
	$host="localhost";
	$port=3306;
	$socket="";
	$user="lrb_web";
	$password="zmRpRb4qmbTL0Ke7";
	$dbname="lect_reg_base";
	$data="";
	$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
		or die ('Could not connect to the database server' . mysqli_connect_error());
	$result = mysqli_query($con, "CALL `lect_reg_base`.`GET_TEACHER_LECTURES`(".$id.");") or die("Query fail: " . mysqli_error());
	$finfo = mysqli_fetch_fields($result);
	foreach ($finfo as $val) {
		switch ($val->name) {

			
			case SUBJECT_CODE:
				$data .='<table class="table table-bordered"> <tr><th>Ainekood</th>';
				break;
			case LECTURE_ID:
				$data .='<th>Loengu ID</th>';
				break;
			case LECTURE_INFO:
				$data .= '<th>Loengu info</th>';
				break;
			case LECTURE_START_TIME:
				$data .= '<th>Loengu algusaeg</th>';
				break;
			case LECTURE_END_TIME:
				$data .= '<th>Loengu l'.chr(244).'puaeg</th></tr>';
				break;			
		}
    }
	echo $data;
	 while ($row = mysqli_fetch_array($result)){   
		echo '<tr><td>'.$row[0].'</td><td>'.$row[1].'</td><td>'.$row[2].'</td><td>'.$row[3].'</td><td>'.$row[4].'</td></tr>'; 
	}
	echo '</table>';
}



if ($_POST["export"]==1){
	echo "sep=, \n";
	if ($_POST["selection"]==1){
		tocsv("CALL `lect_reg_base`.`GET_LECTURE_ATTENDEES`(".$_POST["value"].")",$_POST["value"]);
	}
	else if ($_POST["selection"]==2){	
		tocsv("CALL `lect_reg_base`.`GET_SUBJECT_LECTURES`(".'"'.$_POST["value"].'"'.")",$_POST["value"]);
	}
	else if ($_POST["selection"]==3){	
		tocsv("CALL `lect_reg_base`.`GET_USER_ATTENDANCE`(".$_POST["value"].")",$_POST["value"]);
	}
	else if ($_POST["selection"]==4){	
		tocsv("CALL `lect_reg_base`.`GET_TEACHER_LECTURES`(".$_POST["value"].");",$_POST["value"]);
	}
}
else{
	//echo '<head><meta charset="UTF-8"></head>';
	echo '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">';
	if ($_POST["selection"]==1){
		attendees($_POST["value"]);
	}
	else if ($_POST["selection"]==2){	
		subject_lect($_POST["value"]);
	}
	else if ($_POST["selection"]==3){	
		attendance($_POST["value"]);
	}
	else if ($_POST["selection"]==4){	
		lecturer($_POST["value"]);}
	}
?>