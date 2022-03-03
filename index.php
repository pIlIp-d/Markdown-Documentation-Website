<!DOCTYPE html>
<html>
    <body>
        <h1 id="documentation-website">Documentation Website</h1>
    
        <?php 
        ini_set('display_errors', 1);
        if (isset($_GET['rebuild'])){ 
            $out = shell_exec('python3 /var/www/website/build_website.py');
            echo $out;
            echo "<form action='/index.php' method='get'></form><script>location.href = location.href.split('?')[0]</script>";
            }
        ?>
        <form action='/index.php' method='get'><input id='rebuild_btn' type='submit' name='rebuild' value='Build HTML'></form>
    </body>
</html>
