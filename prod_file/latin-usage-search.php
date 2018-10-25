<!doctype html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	
	<!-- Image for tab and title of page. -->
	<link rel="icon" href="./resources/favicon.jpg">
	<title>CS5970 Project 1</title>
    <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            }
        th, td {
            padding: 15px;
            }
        th {
            text-align: left;
            }
        .bargraph {
            list-style: none;
            width:960px;
            }
        ul.bargraph li {
            height: 35px;
            text-align: left;
            font-style: italic;
            font-weight:bolder;
            font-size: 14px;
            line-height: 35px;
            padding: 0px 20px;
            margin-bottom: 5px;
            background: #97B546;
            }
    </style>
</head>
<body style="margin: 3em;">
    <div style="padding: 0 0 3em 0; ">
        <a href="latin-term-search.php"> Term Search </a>&nbsp;&nbsp;&nbsp;
        <a href="latin-usage-search.php"> Usage Chart </a>&nbsp;&nbsp;&nbsp;
    </div>
    <form method="GET" action="latin-usage-search.php">
        Please enter the word that you want to search in the latin text: <br/><br/>
        <input type="text" name="word" placeholder="Word to search for..." minlength=1 required autofocus/> <br/> <br/>
        <input type="radio" name="lang" value="lat" checked/>Latin &nbsp;&nbsp; 
        <input type="radio" name="lang" value="eng"/>English <br/> <br/>
        <input type="submit" name="sub-btn" value="SUBMIT"/> <br/>

    </form>

<?php
function getData($word){
        $collection = array();
        $min = 9999;
        $max = 0;
        $db = new SQLite3("latinworks.db") or die("can't connect to database");
        $count_query = "SELECT count(*) from latinworks_fts4 where passage match '" . $word . "';";
        $query = "SELECT title, count(link) from latinworks_fts4 where passage match '"
                 . $word
                 . "' group by title order by count(link) desc;";
        $count_result = $db->querySingle($count_query);
        if ($count_result == 0){
            echo 'No matches found for "' . $word . '".';
        } else {
            $result = $db->query($query);
            while($row = $result->fetchArray()) {
                $title = $row['title'];
                $count = $row['count(link)'];
                $collection[$title] = $count;
            }
            foreach($collection as $value) {
                if($value < $min) {$min = $value;}
                if($value > $max) {$max = $value;}
            }
            $range = $max - $min;
            echo '<br>&nbsp;&nbsp;&nbsp;&nbsp;For translation: <strong>' . $word . '</strong>';
            echo '<ul class="bargraph">';
            foreach($collection as $key => $value){
                $normalized = ((100 * ($value + 0.1 - $min))/$range);
                echo '<li style="width:' 
                     . $normalized . '%;">' . $key . '('. $value . ')</li>';
            }
            echo '</ul>';
        }
}
    if($_GET["sub-btn"] == "SUBMIT") {
        $translation_arr = array();
        $word = $_GET["word"];
        $lang = $_GET["lang"];
        $lang_expanded = $lang == 'lat' ? " (Latin)" : " (English)";
        echo '<div style="padding: 3em 0 0 0;">Usage results for: <strong>' . $word . '</strong> ' . $lang_expanded . '</div>';
        if ($lang == 'eng') {
            $mymemory = "http://api.mymemory.translated.net/get?q=" . $word . "&langpair=en|la&de=akshaygaur@ou.edu";
            $api_response = file_get_contents($mymemory);
            $trans_json = json_decode($api_response, true);
            if($trans_json["responseStatus"] == 200){
                foreach($trans_json['matches'] as &$translation){
                    if (strcasecmp($translation['segment'], $word) == 0) {
                        $translated_word = $translation['translation'];
                        array_push($translation_arr, $translated_word);
                        getData($translated_word);
                    }
                }
                echo "Translations found for '" . $word . "' : ";
                foreach($translation_arr as $item) {
                    echo "<strong>'" . $item . "'  </strong>";
                }
            }
        } else { getData($word);  }
    }
?>

</body>

</html>

