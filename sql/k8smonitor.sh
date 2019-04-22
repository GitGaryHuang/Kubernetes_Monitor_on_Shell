ARGS=`getopt -o "c:m:f:n:u h" -n "k8smonitor.sh" -- "$@"`

eval set -- "$ARGS"

while true; do
	case "$1" in
		-c)
			shift;
			if [ "$1" = "usage" ]||[ "$1" = "usagerate" ]||[ "$1" = "limit" ]||[ "$1" = "request" ]||[ "$1" = "nodeallocatable" ]||[ "$1" = "nodecapacity" ]||[ "$1" = "nodereservation" ]||[ "$1" = "nodeutilization" ] ;then
				echo -e "\033[34mStart cpu/$1 Monitoring at `date`\033[0m"
				watch -c -n 60 -t python /home/k8s-master/sql/cpu"$1".py
				echo -e "\033[34mFinish cpu/$1 monitoring at `date`\033[0m"
			else
				echo -e "\033[33mWrong Parameter Warning------Found\033[31m \"$1\"\033[0m \033[33min syntax \033[0m"
			fi
			shift;
			break;
			;;
		-f)
			shift;
			if [ "$1" = "inodes" ]||[ "$1" = "inodesfree" ]||[ "$1" = "limit" ]||[ "$1" = "usage" ];then
				echo -e "\033[34mStart filesystem/$1 Monitoring at `date`\033[0m"
				watch -c -n 60 -t python /home/k8s-master/sql/filesystem"$1".py
				echo -e "\033[34mFinish filesystem/$1 Monitoring at `date`\033[0m"
			else
				echo -e "\033[33mWrong Parameter Warning------Found\033[31m \"$1\"\033[0m \033[33min syntax \033[0m"
			fi
			shift;
			break;
			;;
		-m)
			shift;
			if [ "$1" = "cache" ]||[ "$1" = "limit" ]||[ "$1" = "majorpagefaults" ]||[ "$1" = "majorpagefaultsrate" ]||[ "$1" = "nodeallocatable" ]||[ "$1" = "nodecapacity" ]||[ "$1" = "nodereservation" ]||[ "$1" = "nodeutilization" ]||[ "$1" = "pagefaults" ]||[ "$1" = "pagefaultsrate" ]||[ "$1" = "request" ]||[ "$1" = "rss" ]||[ "$1" = "usage" ]||[ "$1" = "workingset" ];then
				echo -e "\033[34mStart memory/$1 Monitoring at `date`\033[0m"
				watch -c -n 60 -t python /home/k8s-master/sql/memory"$1".py
				echo -e "\033[34mFinish memory/$1 monitoring at `date`\033[0m"
			else 
				echo -e "\033[33mWrong Parameter Warning------Found\033[31m \"$1\"\033[0m \033[33min syntax \033[0m"
			fi
			shift;
			break;
			;;
		-n)
			shift;
			if [ "$1" = "rx" ]||[ "$1" = "rxerrors" ]||[ "$1" = "rxerrorsrate" ]||[ "$1" = "rxrate" ]||[ "$1" = "tx" ]||[ "$1" = "txerrors" ]||[ "$1" = "txerrorsrate" ]||[ "$1" = "txrate" ];then
				echo -e "\033[34mStart network/$1 Monitoring at `date`\033[0m"
				watch -c -n 60 -t python /home/k8s-master/sql/network"$1".py
				echo -e "\033[34mFinish network/$1 monitoring at `date`\033[0m"
			else
				echo -e "\033[33mWrong Parameter Warning------Found\033[31m \"$1\"\033[0m \033[33min syntax \033[0m"
			fi
			shift;
			break;
		        ;;
		-u)
			echo -e "\033[34mStart uptime Monitoring at `date`\033[0m"
			watch -c -n 60 -t python /home/k8s-master/sql/uptime.py
			echo -e "\033[34mFinish uptime monitoring at `date`\033[0m"
			shift;
			break;
		        ;;
		-h)
			echo -e "\033[32mK8SMONITOR HELP \033[0m"
			cat /home/k8s-master/sql/help.txt
			shift;
			break;
			;;
		-*)
			echo -e "\033[33mPlease Use \033[36m"\"km -h\""\033[0m \033[33mFor Help \033[0m";
			exit 1 ;; 		
		--)
			shift;
			break;
			;;
	esac
done

