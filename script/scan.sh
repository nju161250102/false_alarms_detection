#! /bin/bash
function usage(){
	echo "Usage: scan.sh -p [Project_id] -b [Bug_id] | -a "
	echo "  (Use -a to handle all projects and bugs)"
}


function scan_one(){
	echo "Poject:$1, Bug:$2"
	target_dir="/tmp/${1,,}_${2}_buggy"
	defects4j checkout -p ${1} -v ${2}b -w ${target_dir}
	cd $target_dir
	defects4j compile
	a=$(ls -lt | grep ^d | head -n 1 | awk '{print $9}')
#	a=$(cat default.properties | grep "build.home")
#	a=${a##* }
	echo ${a}
	~/findbugs-3.0.1/bin/findbugs -textui -jvmArgs "-Xmx2048m" -high -sortByClass -xml -output ~/resultData/${1}_${2}.xml ${target_dir}/${a}/classes
	cd ~
	rm -rf $target_dir
}

while getopts a:p:b: option
do
	case "${option}"  in
		a) ALL=1;;
		p) PID=${OPTARG};;
		b) BID=${OPTARG};;
		?) 
			usage
			exit;;
	esac
done

if test $ALL -eq 1
then
	for project_id in `defects4j pids | tail -n +4`
	do
		for bug_id in `cat ~/defects4j/framework/projects/${project_id}/active-bugs.csv | tail -n +2 |awk -F, '{ print $1; }'`
		do
			scan_one ${project_id} ${bug_id}
		done
	done
else
	scan_one $PID $BID
fi
