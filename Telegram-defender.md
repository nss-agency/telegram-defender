#Telegram-defender

1. This bot can be added to any group or Channel on Telegram.
2. It must announce itself to everyone when they join.
>Hi! I'm Telegram Defender.
>I scan links that get posted for malware, and tell you more about the news source that gets posted, what their
> political bias may be, and if they're fake. Say /td-help for more information.

>/td-help
>For more information on how we work, go here.
>We are all open source.

3. When someone posts a link
    - Scan for Malware
        + If there is malware, delete it and post this message:
        
                🦠 MALWARE DETECTED 🦠 
                This link has been removed.

        + If no malware has been detected, run it against the Allsides JSON.
                - If the source of news is found.
                ✅ NO MALWARE DETECTED! ✅
                Scanned by [DrV.com](drv.com)😷
                This publication has been rated as having a [lean left bias politically](https://www.allsides.com/news-source/washington-post-media-bias)
                {bias-image} • [?](https://www.allsides.com/media-bias/media-bias-ratings?utm_source=Live+Partner+Network&utm_medium=Media+Bias+Ratings&utm_campaign=Telegram+Defender)


.long-version{

"☝️This publication has been rated as having a " + [ option 1-5 ] +"bias politically." [img]""
    1: 
        bias:   "left",
        bias-image:  "./allsides/bias-left.png",
        link:   "https://www.allsides.com/media-bias/left-center",
    2: 
        bias:   "leaning left:",
        bias-image:  "./allsides/bias-leaning-left.png",
        link:   "https://www.allsides.com/media-bias/left-center",
    3:  
        bias:   "center",
        bias-image:  ".allsides/bias-leaning-center.png",
        link:   "https://www.allsides.com/media-bias/center",
    4:
        bias:   "leaning right",
        bias-image:  "./allsides/bias-leaning/right.png",
        link:   "https://www.allsides.com/media-bias/right-center",
    5:
        bias:   "right",
        bias-image:  "./allsides/bias-right.png",
        link:   "https://www.allsides.com/media-bias/right",
    6:
        bias:   "mixed",
        bias-image:  "./allsides/mixed.png",
        link:   "https://www.allsides.com/media-bias/allsides",
}







----





# MAKEFILE

1. Please include a makefile that looks like the following:
    Step 1: Download and install these local dependenceis and frameworks
        - NodeJs
        - Modern Telegram Bot Framework for Node.js 
            + https://github.com/telegraf/telegraf

        - etc
    Step 2: Add in the following scripts and images that we wrote
        - file.txt
        - file.json
        - file.img
    Step 3: Add in the following API keys the the API.txt document
        - malware XXXX
        - allsides XXX

# TODO
- [] Additional APIs
- [] Newstrition Integration
- [] ?utm_source=Live+Partner+Network&utm_medium=Media+Bias+Ratings&utm_campaign=Telegram+Defender

### 



Scanners:
Malware Scanner: https://rapidapi.com/thumbsup/api/malware-scanner
Avira: https://rapidapi.com/rohitk644/api/avira-url-safety-cloud
    > https://aws.amazon.com/marketplace/pp/Avira-Avira-URL-Safety-Cloud/B079C6B7LL

Bitdefender: https://www.bitdefender.com/oem/url-status.html

URL Reputation: https://rapidapi.com/stefan.skliarov/api/Metacert
Asgard: https://rapidapi.com/rollbackup/api/asgard

Bias:
Allsides.com Bias

News:
Hoaxy: https://rapidapi.com/truthy/api/hoaxy
NewsAPI: https://rapidapi.com/raygorodskij/api/NewsAPI

Newstrition 
https://www.freedomforuminstitute.org/first-amendment-center/newstrition/


