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
    </style>
</head>
<body style="margin: 3em;">
    <div style="padding: 0 0 3em 0; ">
        <a href="#" onclick="return false"> Term Search </a>&nbsp;&nbsp;&nbsp;
        <a href="latin-usage-search.php"> Usage Chart </a>&nbsp;&nbsp;&nbsp;
    </div>
    <form method="GET" action="latin-term-search.php">
        Please enter the word that you want to search in the latin text: <br/><br/>
        <input type="text" name="word" placeholder="Word to search for..." minlength=1 required autofocus/> <br/> <br/>
        <input type="radio" name="lang" value="lat" checked/>Latin &nbsp;&nbsp; 
        <input type="radio" name="lang" value="eng"/>English <br/> <br/>
        <input type="submit" name="sub-btn" value="SUBMIT"/> <br/>

    </form>


<?php
function getData($word){

        $db = new SQLite3("latinworks.db") or die("can't connect to database");
        $count_query = "SELECT count(*) from latinworks_fts4 where passage match '" . $word . "'";
        $query = "SELECT passage, link from latinworks_fts4 where passage match '" . $word . "'";
        $count_result = $db->querySingle($count_query);
        if ($count_result == 0){
            echo 'No matches found for "' . $word . '".';
        } else {
            $result = $db->query($query);
            echo '<div style="padding: 3em;">';
            echo "<table>";
            echo "<caption>Matches for ". $word . "</caption>";
            echo "<tr>";
            echo "<th>Passage Excerpt</th>";
            echo "<th>Link</th>";
            echo "</tr>";
            while($row = $result->fetchArray()) {
                $pas = $row['passage'];
                $link = $row['link'];
                $word_pos = strpos($pas, $word);
                $pas_len = strlen($pas);
                $pas_2_show2 = substr($pas, $word_pos + strlen($word), 25);
                $pas_2_show1 = substr($pas, $word_pos - 25, 25);
                //echo "..." . $pas_2_show1 . "<strong>" . $word . "</strong>" . $pas_2_show2 . "...";
                //echo "<br/><br/>";
                //echo "<a href=\"" . $link . "\">" . $link . "</a>" . "<br/>";
                echo "<tr>";
                echo "<td>..." . $pas_2_show1 . "<strong>" . $word . "</strong>" . $pas_2_show2 . "...</td>";
                echo "<td><a href=\"" . $link . "\">" . $link . "</a>" . "</td>";
                echo "</tr>";
            }
            echo "</table>";
            echo "</div>";
        }
}
    if($_GET["sub-btn"] == "SUBMIT") {
        $word = $_GET["word"];
        $lang = $_GET["lang"];
        $lang_expanded = $lang == 'lat' ? " (Latin)" : " (English)";
        echo '<div style="padding: 3em 0 0 0;">Search results for: ' . $word . $lang_expanded . '</div>';
        if ($lang == 'eng') {
            $mymemory = "http://api.mymemory.translated.net/get?q=" . $word . "&langpair=en|la&de=akshaygaur@ou.edu";
            $api_response = file_get_contents($mymemory);
            $trans_json = json_decode($api_response, true);
            if($trans_json["responseStatus"] == 200){
                foreach($trans_json['matches'] as &$translation){
                    if (strcasecmp($translation['segment'], $word) == 0) {
                        getData($translation['translation']);
                    }
                }
            }
        } else { getData($word);  }
    }
?>

</body>

</html>
