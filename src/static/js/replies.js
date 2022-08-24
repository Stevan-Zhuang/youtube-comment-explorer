function setReplies() {
    fetch("static/json/top_filtered_replies.json")
        .then(function(response) {return response.json()})
        .then(function(data) {
            for (ch = 0; ch < data["items"].length; ch++) {
                var channel = data["items"][ch];

                console.log(channel);

                var channel_name = channel["channel_name"] + "\n";
                document.getElementById("replies").innerHTML += channel_name;

                for (rp = 0; rp < channel["comments"].length; rp++) {
                    var reply = channel["comments"][rp];
                    
                    reply_data = reply["content"] + " 👍";
                    reply_data += reply["likes"].toString() + "\n";
                    document.getElementById("replies").innerHTML += reply_data;
                }
            }
        });
}