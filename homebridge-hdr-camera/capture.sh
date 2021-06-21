while true
do
    start_time="$(date -u +%s)"

    # Take a sequence of exposures from 3 s to 1 ms
    raspistill -w 1296 -h 972 -t 10 -bm -ex off -ag 1 -ss 30000000 -st -o images/exp1.png
    raspistill -w 1296 -h 972 -t 10 -bm -ex off -ag 1 -ss 1000000 -st -o images/exp2.png
    raspistill -w 1296 -h 972 -t 10 -bm -ex off -ag 1 -ss 100000 -st -o images/exp3.png
    raspistill -w 1296 -h 972 -t 10 -bm -ex off -ag 1 -ss 10000 -st -o images/exp4.png
    raspistill -w 1296 -h 972 -t 10 -bm -ex off -ag 1 -ss 1000 -st -o images/exp5.png
    enfuse -o images/hdr_latest_in_process.jpg images/exp*.png
    cp  images/hdr_latest_in_process.jpg  hdr_latest.jpg

    # Save the file to Dropbox
    FOLDER="$(date +"%Y_%m_%d")" 
    HOUR="$(date +"%H")" 
    FILE_NAME="$(date +"%FT%T.jpg")"
    OUTFILE="/picams/"$CAMERA_LOCATION"/"$FOLDER"/"$HOUR"/"$FILE_NAME
    echo $OUTFILE
    python3 upload2drobox.py --i hdr_latest.jpg --o "$(echo $OUTFILE)"
    
    # Calculate how long all this took
    end_time="$(date -u +%s)"
    elapsed="$(($end_time-$start_time))"
    echo "Total of $elapsed seconds elapsed for process"

    sleep 5
done
