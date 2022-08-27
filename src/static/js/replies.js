function setReplies() {
    fetch("static/json/top_filtered_replies.json")
        .then(function(response) {return response.json()})
        .then(function(data) {
            for (ch = 0; ch < data["items"].length; ch++) {
                var channel = data["items"][ch];

                var img = document.createElement("img");
                img.src = channel["image_url"]
                var src = document.getElementById("replies");
                src.appendChild(img);

                var channel_name = channel["channel_name"] + "\n";
                document.getElementById("replies").innerHTML += channel_name;

                for (rp = 0; rp < channel["comments"].length; rp++) {
                    var reply = channel["comments"][rp];
                    
                    reply_data = reply["content"] + " 👍";
                    reply_data += reply["likes"].toString() + "\n";
                    reply_data += reply["time_ago"] + "\n"
                    document.getElementById("replies").innerHTML += reply_data;
                }
            }
        });
}