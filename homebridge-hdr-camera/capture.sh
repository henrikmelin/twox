while true
do
    start_time="$(date -u +%s)"
    raspistill -w 1296 -h 972 -hf -vf -t 10 -bm -ex off -ag 1 -ss 30000000 -st -o images/exp1.png
    raspistill -w 1296 -h 972 -hf -vf -t 10 -bm -ex off -ag 1 -ss 1000000 -st -o images/exp2.png
    raspistill -w 1296 -h 972 -hf -vf -t 10 -bm -ex off -ag 1 -ss 100000 -st -o images/exp3.png
    raspistill -w 1296 -h 972 -hf -vf -t 10 -bm -ex off -ag 1 -ss 10000 -st -o images/exp4.png
    raspistill -w 1296 -h 972 -hf -vf -t 10 -bm -ex off -ag 1 -ss 1000 -st -o images/exp5.png
    enfuse -o images/hdr_latest_in_process.jpg images/exp*.png
    cp hdr_last09.jpg hdr_last10.jpg
    cp hdr_last08.jpg hdr_last09.jpg
    cp hdr_last07.jpg hdr_last08.jpg
    cp hdr_last06.jpg hdr_last07.jpg
    cp hdr_last05.jpg hdr_last06.jpg
    cp hdr_last04.jpg hdr_last05.jpg
    cp hdr_last03.jpg hdr_last04.jpg
    cp hdr_last02.jpg hdr_last03.jpg
    cp hdr_last01.jpg hdr_last02.jpg
    cp hdr_latest.jpg hdr_last01.jpg
    cp  images/hdr_latest_in_process.jpg  hdr_latest.jpg

    end_time="$(date -u +%s)"
    elapsed="$(($end_time-$start_time))"
    echo "Total of $elapsed seconds elapsed for process"

    sleep 5
done