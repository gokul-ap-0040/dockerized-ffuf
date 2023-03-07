function generate_wordlist() {
   git clone -q https://$GIT_USERNAME:$GIT_PASSWORD@github.com/shopuptech/$2
   cd $2
   git ls-files > ../$2-wordlist.txt
   cat ../common.txt >> ../$2-wordlist.txt   
   cd ..
   rm -rf $2
}

function bruteforce() {
   ffuf -v -r -mc 200 -u $1/FUZZ -w $2-wordlist.txt -of csv -o $2-o1.txt > out 2>&1
   printf "\n[+] Exposed Files :\n\n"
   cat $2-o1.txt | tail -n +2 | cut -d "," -f3 > $2-o2.txt 2>&1
   rm $2-o1.txt
   rm out
}

function filter_results() {
   cat $1-o2.txt | grep -v '\.\(php\|js\|html\|png\|jpg\|jpeg\|css\|ttf\|gif\|eot\|z\|htm\|docx\|pdf\|woff2\|eot\|svg\|doc\|htm\|woff\|txt\|ico\|fdf\|eps\|icc\|ai\|md\|p12\|otf\|swf\|TXT\|inv\|crt\|psd\|ufm\|afm\|map\|ser\|rst\|ts\|tsx\|lock\)$' | tee $1-output.txt 
}

url=$1 
repo_url=$2 

repo=$(echo $repo_url | cut -d "/" -f5)

################################

generate_wordlist $repo_url $repo
bruteforce $url $repo
filter_results $repo

rm $repo-o2.txt
rm $repo-wordlist.txt

echo "$url, $repo_url" | cat - $repo-output.txt > temp && mv temp $repo-output.txt
python txt2pdf.py $repo-output.txt
