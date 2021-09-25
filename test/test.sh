#!/bin/bash

delay=0
tmp_tw_log=/tmp/test_tw_log.txt
tmp_tem_log=/tmp/test_tem_log.txt
show_progress=0

verbose=0
logs_path=./logs
settings_path=./settings
stdin_log=0
interactive_dbg=0

RESET="\033[0m"
BOLD="\033[1m"

function set_paths() {
	if [ "$1" != "" ]
	then
		if [ "$1" == "-" ]
		then
			stdin_log=1
			logs_path="/dev/stdin"
			echo "reading logs from stdin."
			return
		fi
		if [ ! -d "$1" ]
		then
			echo "Error logs path not found '$1'"
			exit 1
		fi
		logs_path="$1"
		echo "using custom logs path: $1"
	fi
	if [ "$2" != "" ]
	then
		if [ ! -d "$2" ]
		then
			echo "Error settings path not found '$2'"
			exit 1
		fi
		settings_path="$2"
		echo "using custom settings path: $2"
	fi
}

if [ "$1" == "--help" ] || [ "$1" == "-h" ]
then
	echo    "usage: $0 [OPTION] [LOG_DIR] [SETTINGS_DIR]"
	echo    "  arguments:"
	echo -e "    OPTION       - ${BOLD}-h${RESET} Show this help page."
	echo -e "                   ${BOLD}-v${RESET} Verbose output."
	echo -e "                   ${BOLD}-i${RESET} Interactive debugging on error."
	echo -e "                   ${BOLD}-p${RESET} Show progress (for long logs)."
	echo -e "                   ${BOLD}--help${RESET} Equivalent to ${BOLD}-h${RESET}."
	echo -e "                   ${BOLD}--verbose${RESET} Equivalent to ${BOLD}-v${RESET}."
	echo -e "                   ${BOLD}--interactive${RESET} Equivalent to ${BOLD}-i${RESET}."
	echo -e "                   ${BOLD}--progress${RESET} Equivalent to ${BOLD}-p${RESET}."
	echo    "    LOG DIR      - Path to directory containing tw .log files."
	echo -e "                   ${BOLD}-${RESET} to use stdin."
	echo    "                   default: logs"
	echo    "    SETTINGS DIR - Path to directory containing tem .test files."
	echo    "                   default: settings"
	echo    "  description:"
	echo    "    Pipes all logs-settings combinations into tem python script."
	echo    "    Script should be executed from tem_source_root/test for all paths to work."
	echo    "  examples:"
	echo -e "    ${BOLD}$0 --verbose${RESET}"
	echo    "       Run tests with default settings and logs dir and give verbose output." 
	echo    ""
	echo -e "    ${BOLD}$0${RESET} /tmp/logs /tmp/settings"
	echo    "       Run tests with custom logs and settings path."
	echo    ""
	echo -e "    cat /tmp/log.txt | ${BOLD}$0 -${RESET}"
	echo    "       Read log from stdin with default settings path."
	echo    "  bugs:"
	echo    "       stdin log can not be combined with interactive debugger."
	exit
elif [ "$1" == "--verbose" ] || [ "$1" == "-v" ]
then
	verbose=1
	set_paths "$2" "$3"
elif [ "$1" == "--interactive" ] || [ "$1" == "-i" ]
then
	interactive_dbg=1
	set_paths "$2" "$3"
elif [ "$1" == "--progress" ] || [ "$1" == "-p" ]
then
	show_progress=1
	set_paths "$2" "$3"
else
	set_paths "$1" "$2"
fi

failed=0
passed=0
total_logs=0
current_log_line=0

function print_log_lines() {
	current_log_line=0
	echo "" > "$tmp_tw_log"
	while IFS= read -r line
	do
		echo "$line" >> "$tmp_tw_log"
		echo "$line"
		if [[ ! $line =~ '[datafile]'|'[register]'|'[engine/mastersrv]'|'[storage]'|'[econ]'|'[engine]' ]]
		then
			if [ "$delay" == "1" ]
			then
				sleep 0.1
			fi
		fi
		current_log_line=$((current_log_line+1))
		if [ $show_progress -eq 1 ]
		then
			if ! ((current_log_line % 10))
			then
				# worst hack to use stderr to bypass all the redirect and subshell madness
				>&2 echo "lines processed $current_log_line at log $total_logs ..."
			fi
		fi
	done < "$1"
}

mkdir -p stats

# TODO: refactor this mess
function check_interactive_dbg() {
	if [ $interactive_dbg -ne 1 ]
	then
		return
	fi
	echo "[ === ] Interactive debugging [ === ]"
	echo "Examine shell variables using the echo command:"
	echo -e "${BOLD}cat \$tw_log${RESET}"
	echo -e "${BOLD}cat \$tem_log${RESET}"
	echo -e "${BOLD}bt${RESET} to backtrace."
	echo -e "${BOLD}q${RESET} to quit."
	echo "$tem_lines" > "$tmp_tem_log"
	initfile="tw_log='$tmp_tw_log';"
	initfile+="tem_log='$tmp_tem_log';"
	initfile+="function tem_help() { "
	initfile+="echo '[ === ] Interactive debugging [ === ]';"
	initfile+="echo -e \"${BOLD}cat \$tw_log${RESET}\";"
	initfile+="echo -e \"${BOLD}cat \$tem_log${RESET}\";"
	initfile+="};"
	initfile+="function bt() { "
	initfile+="echo '[ === ] Backtrace [ === ]';"
	initfile+="echo -e \"${BOLD}teeworlds log:${RESET}\";"
	initfile+="tail -n10 $tmp_tw_log;"
	initfile+="echo -e \"${BOLD}tem log:${RESET}\";"
	initfile+="tail -n10 $tmp_tem_log;"
	initfile+="};"
	initfile+="alias help=tem_help;"
	initfile+="alias q=exit;"
	initfile+="alias quit=exit;"
	initfile+="PS1='.\$ ';"
	bash --init-file <(echo "$initfile")
	echo "aborting tests due to interactive debugging session."
	exit 0
}

function test_log() {
	log=$1
	setting=$2
	echo   "+---------------------------------------+"
	printf "| log: %-32s |\n" "$log"
	echo   "+---------------------------------------+"
	show_lines=$verbose
	tem_lines=$(print_log_lines "$log" | ../src/main.py --settings="$setting")
	if [ $? -eq 0 ]
	then
		printf "[\033[0;32mSUCCESS\033[0m]\n"
		passed=$((passed+1))
	else
		printf "[\033[0;31mFAILED\033[0m]\n"
		failed=$((failed+1))
		show_lines=1
		check_interactive_dbg
	fi
	if [ "$show_lines" == "1" ]
	then
		echo " === setting: $setting === "
		cat "$setting"
		echo " ================ "
		echo "$tem_lines"
	fi
	total_logs=$((total_logs+1))
}

start_ts="$(date +%s.%N)"

if [ $stdin_log -eq 1 ]
then
	for setting in "$settings_path"/*.test
	do
		test_log "$logs_path" "$setting"
	done
else
	for log in "$logs_path"/*.log
	do
		for setting in "$settings_path"/*.test
		do
			test_log "$log" "$setting"
		done
	done
fi

# timestamp credits go to jwchew
# https://unix.stackexchange.com/a/88802
end_ts="$(date +%s.%N)"

dt=$(echo "$end_ts - $start_ts" | bc)
dd=$(echo "$dt/86400" | bc)
dt2=$(echo "$dt-86400*$dd" | bc)
dh=$(echo "$dt2/3600" | bc)
dt3=$(echo "$dt2-3600*$dh" | bc)
dm=$(echo "$dt3/60" | bc)
ds=$(echo "$dt3-60*$dm" | bc)

echo ""
printf "Total runtime: %d:%02d:%02d:%02.4f\n" "$dd" "$dh" "$dm" "$ds"
printf "failed: \033[0;31m %d/%d \033[0m\n" "$failed" "$total_logs"
printf "passed: \033[0;32m %d/%d \033[0m\n" "$passed" "$total_logs"

if [ $failed -gt 0 ]
then
	exit 1
fi
