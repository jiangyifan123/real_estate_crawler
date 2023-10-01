#!/bin/bash
#descripion: 描述

myPath="/path/to/appdata/config/project/real-est/real_estate_crawler/webcrawler/ZillowCrawler"
crawlerFile="${myPath}/getZillowHTML.py"
cd $myPath
echo $(date +%Y-%m-%d" "%H:%M:%S) "start crawler task" >> "test.txt"
source "${myPath}/ZillowCrawler/bin/activate"
/path/to/appdata/config/project/real-est/real_estate_crawler/webcrawler/ZillowCrawler/ZillowCrawler/bin/python $crawlerFile
echo $(date +%Y-%m-%d" "%H:%M:%S) "end crawler task" >> "test.txt"
