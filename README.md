# Steam Comment Extractor
Extract and archive comments from a Steam Community page. 

To use: `python3 steam_comment_extractor.py YOUR_STEAM64ID_HERE`

You can get your Steam64ID from using a website like [this.](https://steamid.xyz/)

It will extract all the given profile's comments to json, in this format:

    {
        "timestamp": "27 December, 2010 @ 12:56:39 am PST",
        "text": "First.",
        "author": "Ryan",
        "author_link": "https://steamcommunity.com/id/ryan"
    }

Feel free to make issues or contribute but I don't have much interest in working on this beyond the initial version as it has served its purpose. cheers!
